from django.http import StreamingHttpResponse
import base64
import time
import cv2
import os
import json 
import supervision as sv 
from ultralytics import YOLO
import numpy as np 
from enum import Enum
from ..serializer import serializeBusCentroid
from supervision import Position
from queue import Queue
from datetime import datetime
from .getNextBus import getNextBus

# VIDEO_PATH = r"C:/Users/LENOVO/OneDrive/Documents/GitHub/Bus-Stop-Crowd-Detection/data/raw/videos/cctv/LeaveNGoInBus1.mp4"
VIDEO_PATH = r"C:/Users/LENOVO/OneDrive/Documents/GitHub/Bus-Stop-Crowd-Detection/data/raw/videos/cctv/D.mp4"
MODEL_PATH = r"object_detection/model/yolov8l.pt"
LEG_DETECTOR_PATH = r"object_detection/model/legDetector.pt"
# LEG_DETECTOR_PATH = r"C:/Users/LENOVO/OneDrive/Documents/GitHub/Bus-Stop-Crowd-Detection/src/backend/object_detection/model/legDetector.pt"

REGION = {
    "5": 671,
    "4": 1761,
}

# the tolerance window can be accept for the centroid different 
TOLERANCE = 13

model = YOLO(MODEL_PATH)
legDetector = YOLO(LEG_DETECTOR_PATH)
tracker = sv.ByteTrack()
trackerPerson = sv.ByteTrack()
colorAnnotator = sv.ColorAnnotator()
lineAnnotator = sv.LineZoneAnnotator(thickness=1, text_scale=0.5, text_thickness=1)
triAnnotator = sv.TriangleAnnotator(height=20, base=20)

lineZoneList = {
    "4" : {
        "lineZone" : sv.LineZone(
            start = sv.Point(x=1557, y=797),
            end = sv.Point(x=1557, y=526),
            triggering_anchors=(Position.CENTER, Position.CENTER)
        ),
        "xyxy" : [1509, 526, 1808, 797], # top-left bottom-right for cropping region 
    }, 
    "5" : {
        "lineZone" : sv.LineZone(
            start = sv.Point(x=483, y=669),
            end = sv.Point(x=483, y=434), 
            triggering_anchors=(Position.CENTER, Position.CENTER)
        ),
        "xyxy" : [337, 432, 682, 672],
    },
}

# use to store the bus current location id : {centroid, numberMatch, station, status}
busCentroid = {} 
avgLeg = []
inQueue = Queue(maxsize=10)
numberOfPpl = 0
currentFrameIndex = 0
busStationTime = {
    "Station 4" : {},
    "Station 5" : {}
}

class BusStatus(Enum):
    NO_DETECT = "No bus detected" # wont be used, if dont have bus then centroid will be empty 
    LEAVE_BUS = "Passengers on the bus are getting off"
    WAITING = "Wait for passengers to board" # wait when have ppl up / after ppl down / after resting 
    DETECTING = "Detecting"
    LEAVING = "The bus is leaving for the next stop"
    
    def __str__(self) :
        return self.value

def isBusExist(result) :
    return True if len(result[0].boxes.xyxy) > 0 else False

# clear when the bus is leaving  
def clearBusLocation() : 
    global busCentroid
    busCentroid = {}

def isBusCentroidExist(busId, centroid = busCentroid) : 
    return busId in centroid

# match the tolerance windown
def isWithinRange(currentCentroid, prevCentroid, tolerance = TOLERANCE) : 
    # calculate the euclidean distance between current and previous  
    euclideanDistance = np.linalg.norm(prevCentroid - currentCentroid)
    return euclideanDistance <= tolerance

def updateBusStatus(busId, status) : 
    global busCentroid 
    busCentroid[busId]["status"] = status

def getRegion(centroidX) : 
    for x in REGION :
        if centroidX < REGION[x] : 
            return x
    # outside station 4 and 5 
    return None 

def isLeave(bbox) : 
    # check bus xyxy is outside the x of station 4
    # if outside means already leave 
    # bbox[3] = bottom right corner 
    return bbox[2] >= REGION["4"]

def cleanLineZone(station) : 
    global lineZoneList
    # clean the lineZone
    lineZoneList[station]["lineZone"] =  sv.LineZone(
            start = sv.Point(x=1557, y=797),
            end = sv.Point(x=1557, y=526),
            triggering_anchors=(Position.CENTER, Position.CENTER)
        )
    # lineZoneList[station]["lineZone"].out_count = 0

def getCropFrame(frame, bbox) : 
    cropLeft = bbox[0]
    cropRight = bbox[2]
    cropTop = bbox[1]
    cropBottom = bbox[3]

    # crop 
    return frame[cropTop:cropBottom, cropLeft:cropRight], cropLeft, cropTop

def getBoundingBoxForGlobal(xyxy, cropLeft, cropTop) : 
    offsetBoxes = []
    for box in xyxy:
        lx1, ly1, lx2, ly2 = box
        gx1 = lx1 + cropLeft
        gy1 = ly1 + cropTop
        gx2 = lx2 + cropLeft
        gy2 = ly2 + cropTop
        offsetBoxes.append([gx1, gy1, gx2, gy2])

    # Convert to NumPy array with shape (N,4) or (0,4)
    return np.array(offsetBoxes, dtype=float).reshape(-1, 4)

def isOverlapping(aDict, bDict) : 
    # abbox[0] < bcentroid[0] and abbox[2] > bcentroid[0] and  # this will be removed since already done in quick check 
    return aDict["station"] == bDict["station"] and aDict["status"] == bDict["status"] and (aDict["status"] == BusStatus.WAITING or aDict["status"] == BusStatus.LEAVE_BUS)

def checkOverlapping(centroid, busId) : 
    global busCentroid

    for b in busCentroid : 
        if b != busId :
            # id not same 
            # check do busId have overlap with who 
            # busId will be b sice b is the one be checked 
            # quick check 
            print(f"b = {b} vs {busId} : {busCentroid[b]["xyxy"][0]} < {centroid[0]} < {busCentroid[b]["xyxy"][2]}")
            if busCentroid[b]["xyxy"][0] < centroid[0] < busCentroid[b]["xyxy"][2] : 
                if isOverlapping(busCentroid[b], busCentroid[busId]) : 
                    return True
    return False

def videoProcess(request):
    # check filepath exist 
    if not os.path.exists(VIDEO_PATH) : 
        # not exist raise an error 
        raise FileNotFoundError("Video doesnot exist")

    def generate():
        global currentFrameIndex
        global busStationTime
        
        cap = cv2.VideoCapture(VIDEO_PATH)
        # simple safety check in case the video fails to open
        if not cap.isOpened():
            print("Error opening video stream or file")
            yield "data: \n\n"
            return
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, currentFrameIndex)

        while True:
            ret, frame = cap.read()
            if not ret:
                # if reach the end of the video, we can loop from the start
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                currentFrameIndex = 0
                continue
            
            # detect human and bus
            result = model(frame, classes=[5])

            # check bus exist 
            if isBusExist(result) : 
                # bus exist - check moving 
                detections = sv.Detections.from_ultralytics(result[0])
                tracks = tracker.update_with_detections(detections)
                annotatedFrame = colorAnnotator.annotate(scene=frame.copy(), detections=detections)
                
                # calculate current number of ppl in queue 
                # take avg 
                numberOfPpl = 0
                if not inQueue.empty() : 
                    for q in inQueue.queue : 
                        numberOfPpl += q
                    
                    numberOfPpl = int(numberOfPpl / inQueue.qsize())
                
                busIdList = []
                # loop track get centroid
                for track in tracks : 
                    # get id and boundary box 
                    busId = str(track[4])
                    busIdList.append(busId)

                    bbox = track[0]

                    # calculate center 
                    centerX = (bbox[0] + bbox[2])/2
                    centerY = (bbox[1] + bbox[3])/2

                    currentLocation = np.array([centerX, centerY])
                    if not isBusCentroidExist(busId) : 
                        # busid doesnot exist in the dictionary - create one 
                        # init 
                        now = datetime.now()
                        busCentroid[busId] = {}
                        busCentroid[busId]["centroid"] = currentLocation
                        busCentroid[busId]["xyxy"] = bbox
                        busCentroid[busId]["numberMatch"] = 0
                        busCentroid[busId]["station"] = None
                        busCentroid[busId]["passengerInBus"] = 0
                        busCentroid[busId]["passengerLeaveBus"] = 0
                        busCentroid[busId]["busNoExist"] = 0 # how many frame doesnot exist ( over 5 remove it )
                        busCentroid[busId]["busArrivalTime"] = now.strftime("%H:%M:%S")
                        updateBusStatus(busId, BusStatus.DETECTING)
                    else :  
                        
                        if len(busCentroid) == 1 or not checkOverlapping(centroid=currentLocation, busId=busId) : 
                            # compare busCentroid, if same for 10 frame means stopping, else store the busCentroid and status = moving 
                            # counter 
                            prevLocation = busCentroid[busId]["centroid"]
                            if isWithinRange(currentCentroid=currentLocation, prevCentroid=prevLocation) : 
                                # within the tolerance window 
                                # update the value 
                                busCentroid[busId]["numberMatch"] += 1

                                if busCentroid[busId]["numberMatch"] >= 10 : 
                                    busCentroid[busId]["xyxy"] = bbox
                                    # means stopping - by default set as waiting passenger leave 
                                    updateBusStatus(busId, BusStatus.LEAVE_BUS)
                                    
                                    croppedFrame, cropLeft, cropTop = getCropFrame(frame=frame, bbox=lineZoneList[busCentroid[busId]["station"]]["xyxy"])

                                    # detect person 
                                    passengerResults = model(croppedFrame, classes=[0])  
                                    passengerDetectionsLocal = sv.Detections.from_ultralytics(passengerResults[0])

                                    # create a new bounding box that match with the global frame size 
                                    offsetBoxes = getBoundingBoxForGlobal(passengerDetectionsLocal.xyxy, cropLeft, cropTop)
                                    passengerDetectionsGlobal = sv.Detections(
                                        xyxy=offsetBoxes,
                                        confidence=passengerDetectionsLocal.confidence,
                                        class_id=passengerDetectionsLocal.class_id
                                    )

                                    passengerDetectionsGlobal = trackerPerson.update_with_detections(passengerDetectionsGlobal)

                                    # update the linezone counting by using the original frame 
                                    lineZoneList[busCentroid[busId]["station"]]["lineZone"].trigger(passengerDetectionsGlobal)
                                    print(f"Bus {busId} => People crossing line: in={lineZoneList[busCentroid[busId]["station"]]["lineZone"].in_count}, out={lineZoneList[busCentroid[busId]["station"]]["lineZone"].out_count}")

                                    # # If >2 people come in => WAITING
                                    # if in the queue ppl .... 
                                    if lineZoneList[busCentroid[busId]["station"]]["lineZone"].in_count > 2 :
                                        updateBusStatus(busId, BusStatus.WAITING)

                                    # annonated - for person
                                    annotatedFrame = colorAnnotator.annotate(
                                        scene=annotatedFrame.copy(),
                                        detections=passengerDetectionsGlobal
                                    )

                                    # for line 
                                    annotatedFrame = lineAnnotator.annotate(
                                        annotatedFrame.copy(),
                                        line_counter=lineZoneList[busCentroid[busId]["station"]]["lineZone"]
                                    )

                                else : 
                                    # not reach 10 
                                    updateBusStatus(busId, BusStatus.DETECTING)
                            else : 
                                # because not match means is moving so clear the numberMatch 
                                busCentroid[busId]["numberMatch"] = 0 
                                busCentroid[busId]["centroid"] = currentLocation
                                busCentroid[busId]["lineZone"] = None

                                # check is leave or just only moving 
                                if busCentroid[busId]["status"] == BusStatus.WAITING or busCentroid[busId]["status"] == BusStatus.LEAVE_BUS : 
                                    # if previous data is waiting means now is leave 
                                    updateBusStatus(busId, BusStatus.LEAVING)
                                else : 
                                    # just moving 
                                    updateBusStatus(busId, BusStatus.DETECTING)

                    # do station checking
                    # if station have value then move means is ready to leave 
                    # only will have 3 case , station = None / station == tempStation / station != tempStation 
                    tempStation = getRegion(busCentroid[busId]["centroid"][0])
                    if busCentroid[busId]["station"] is None or (busCentroid[busId]["status"] != BusStatus.LEAVING and busCentroid[busId]["status"] != BusStatus.WAITING) : 
                        # since waiting and leaving wont affect the station 
                        # resting also wont
                        busCentroid[busId]["station"] = tempStation

                    if isLeave(bbox) : 
                        # check the xyxy is outside already or not 
                        # if yes then clear the busCentroid
                        # remove the bus from centroid and get next bus schedule time 
                        bus = busCentroid.pop(busId, None)
                        if bus is not None :
                            cleanLineZone(bus["station"])

                    # ------------------------------------ extra annotated for testing --------------------------------- #
                    # draw bounding box
                    x_min, y_min, x_max, y_max = map(int, bbox)
                    
                    # green box
                    cv2.rectangle(annotatedFrame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  

                    # display Bus ID, Status, and Station
                    text = (f"ID: {busId}, "
                            f"Status: {busCentroid[busId]['status']}, "
                            f"Station: {busCentroid[busId]['station']}")
                    cv2.putText(annotatedFrame, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    # red dot for centroid
                    cv2.circle(annotatedFrame, (int(centerX), int(centerY)), 5, (0, 0, 255), -1)  
                
                # do checking 
                for bid in busCentroid : 
                    if bid not in busIdList : 
                        # add busNoExist
                        busCentroid[bid]["busNoExist"] += 1
                    else : 
                        # remove from bid 
                        busIdList.remove(bid)
                
                # remove if more than 5 times doesnot exist 
                for bid in busIdList : 
                    if busCentroid[bid]["busNoExist"] == 5 :
                        # remove it 
                        bus = busCentroid.pop(bid, None)
                        cleanLineZone(bus["station"])

                # reset busIdList 
                busIdList = []
            else : 
                # dont have bus - detect the number of person by leg detector  
                # crop image , only want the leg 
                xyxy = [0, 480, 1813, 798]
                croppedFrame, cropLeft, cropTop = getCropFrame(frame=frame, bbox=xyxy)

                # apply to leg detect - only have one class
                result = legDetector(croppedFrame)
                legDetectionsLocal = sv.Detections.from_ultralytics(result[0])

                # create bbox for global 
                offsetBoxes = getBoundingBoxForGlobal(legDetectionsLocal.xyxy, cropLeft, cropTop)
                legDetectionsGlobal = sv.Detections(
                    xyxy=offsetBoxes,
                    confidence=legDetectionsLocal.confidence,
                    class_id=legDetectionsLocal.class_id
                )

                legDetectionsGlobal = tracker.update_with_detections(legDetectionsGlobal)

                # annotated
                annotatedFrame = triAnnotator.annotate(scene=frame.copy(), detections=legDetectionsGlobal)

                numberOfPpl = len(offsetBoxes)
            
                if inQueue.full() :
                    # remove 1 value  
                    inQueue.get()
                inQueue.put(numberOfPpl)
            
            # get the bus schedule data 
            if currentFrameIndex % 10 == 0 :
                res = getNextBus("Station 4")
                if res is not None:
                    assignmentFour, busFour = res
                    busStationTime["Station 4"] = {}
                    busStationTime["Station 4"]["nextBusTime"] = assignmentFour["Time"]
                    busStationTime["Station 4"]["busCarPlateNo"] = busFour["CarPlateNo"]
                    busStationTime["Station 4"]["busCapacity"] = busFour["Capacity"]
                else:
                    # Handle the scenario gracefully when there's no next bus
                    assignmentFour, busFour = None, None
                    print("No next bus found for Station 4")
                    busStationTime["Station 4"] = {}
                    busStationTime["Station 4"]["nextBusTime"] = None
                    busStationTime["Station 4"]["busCarPlateNo"] = None
                    busStationTime["Station 4"]["busCapacity"] = None

                res = getNextBus("Station 5")
                if res is not None:
                    assignmentFour, busFour = res
                    busStationTime["Station 5"] = {}
                    busStationTime["Station 5"]["nextBusTime"] = str(assignmentFour["Time"])
                    busStationTime["Station 5"]["busCarPlateNo"] = busFour["CarPlateNo"]
                    busStationTime["Station 5"]["busCapacity"] = str(busFour["Capacity"])
                else:
                    # Handle the scenario gracefully when there's no next bus
                    assignmentFour, busFour = None, None
                    print("No next bus found for Station 5")
                    busStationTime["Station 5"] = {}
                    busStationTime["Station 5"]["nextBusTime"] = None
                    busStationTime["Station 5"]["busCarPlateNo"] = None
                    busStationTime["Station 5"]["busCapacity"] = None
            # ----------------------------------- start sending data to frontend ------------------------------------- #
            # encode frame to JPEG
            _, jpeg_frame = cv2.imencode('.jpg', annotatedFrame)

            # convert to base64 to send over SSE
            b64_frame = base64.b64encode(jpeg_frame.tobytes()).decode('utf-8')

            # serialize because cant pass int or numeric value 
            sBusCentroid = serializeBusCentroid(busCentroid=busCentroid, lineZoneList=lineZoneList)

            data = {
                "frame": b64_frame,
                "num_people": numberOfPpl,
                "busCentroid": sBusCentroid,
                "busStationTime": busStationTime
            }

            currentFrameIndex = cap.get(cv2.CAP_PROP_POS_FRAMES)

            yield f"data: {json.dumps(data)}\n\n"

            # sleep time 
            # time.sleep(0.05)

    # send SSE
    return StreamingHttpResponse(generate(), content_type='text/event-stream')
