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

# VIDEO_PATH = r"C:/Users/LENOVO/OneDrive/Documents/GitHub/Bus-Stop-Crowd-Detection/data/raw/videos/cctv/LeaveNGoInBus1.mp4"
VIDEO_PATH = r"C:/Users/LENOVO/OneDrive/Documents/GitHub/Bus-Stop-Crowd-Detection/data/raw/videos/cctv/B.mp4"
MODEL_PATH = r"object_detection/model/yolov8l.pt"
LEG_DETECTOR_PATH = r"../../results/weights/best.pt"
REGION = {
    "5": 671,
    "4": 1761,
}

# the tolerance window can be accept for the centroid different 
TOLERANCE = 13

model = YOLO(MODEL_PATH)
tracker = sv.ByteTrack()
trackerPerson = sv.ByteTrack()
colorAnnotator = sv.ColorAnnotator()
lineAnnotator = sv.LineZoneAnnotator(thickness=1, text_scale=0.5, text_thickness=1)

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
currentFrameIndex = 0

class BusStatus(Enum):
    NO_DETECT = "No bus detected" # wont be used, if dont have bus then centroid will be empty 
    LEAVE_BUS = "Passengers on the bus are getting off"
    WAITING = "Wait for passengers to board" # wait when have ppl up / after ppl down / after resting 
    RESTING = "The bus driver is taking a break"
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

def getCropFrame(frame, bbox) : 
    cropLeft = bbox[0]
    cropRight = bbox[2]
    cropTop = bbox[1]
    cropBottom = bbox[3]

    # crop 
    return frame[cropTop:cropBottom, cropLeft:cropRight], cropLeft, cropTop

def videoProcess(request):
    # check filepath exist 
    if not os.path.exists(VIDEO_PATH) : 
        # not exist raise an error 
        raise FileNotFoundError("Video doesnot exist")

    def generate():
        global currentFrameIndex
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

                # loop track get centroid
                for track in tracks : 
                    # get id and boundary box 
                    busId = str(track[4])
                    bbox = track[0]

                    # calculate center 
                    centerX = (bbox[0] + bbox[2])/2
                    centerY = (bbox[1] + bbox[3])/2

                    currentLocation = np.array([centerX, centerY])

                    if not isBusCentroidExist(busId) : 
                        # busid doesnot exist in the dictionary - create one 
                        # init 
                        busCentroid[busId] = {}
                        busCentroid[busId]["centroid"] = currentLocation
                        busCentroid[busId]["numberMatch"] = 0
                        busCentroid[busId]["station"] = None
                        busCentroid[busId]["lineZone"] = None
                        busCentroid[busId]["noOfPassenger"] = -1
                        updateBusStatus(busId, BusStatus.DETECTING)
                    else :  
                        # compare busCentroid, if same for 10 frame means stopping, else store the busCentroid and status = moving 
                        # counter 
                        prevLocation = busCentroid[busId]["centroid"]
                        if isWithinRange(currentCentroid=currentLocation, prevCentroid=prevLocation) : 
                            # within the tolerance window 
                            # update the value 
                            busCentroid[busId]["numberMatch"] += 1

                            if busCentroid[busId]["numberMatch"] >= 10 : 
                                # means stopping - by default set as waiting passenger leave 
                                updateBusStatus(busId, BusStatus.LEAVE_BUS)
                                
                                croppedFrame, cropLeft, cropTop = getCropFrame(frame=frame, bbox=lineZoneList[busCentroid[busId]["station"]]["xyxy"])

                                # detect person 
                                passengerResults = model(croppedFrame, classes=[0])  
                                passengerDetectionsLocal = sv.Detections.from_ultralytics(passengerResults[0])

                                # create a new bounding box that match with the global frame size 
                                offsetBoxes = []
                                for box in passengerDetectionsLocal.xyxy:
                                    lx1, ly1, lx2, ly2 = box
                                    gx1 = lx1 + cropLeft
                                    gy1 = ly1 + cropTop
                                    gx2 = lx2 + cropLeft
                                    gy2 = ly2 + cropTop
                                    offsetBoxes.append([gx1, gy1, gx2, gy2])

                                # Convert to NumPy array with shape (N,4) or (0,4)
                                offsetBoxes = np.array(offsetBoxes, dtype=float).reshape(-1, 4)
                                passengerDetectionsGlobal = sv.Detections(
                                    xyxy=offsetBoxes,
                                    confidence=passengerDetectionsLocal.confidence,
                                    class_id=passengerDetectionsLocal.class_id
                                )

                                # 5) Track people in the global frame
                                passengerDetectionsGlobal = trackerPerson.update_with_detections(passengerDetectionsGlobal)

                                # update the linezone counting by using the original frame 
                                lineZoneList[busCentroid[busId]["station"]]["lineZone"].trigger(passengerDetectionsGlobal)
                                print(f"Bus {busId} => People crossing line: in={lineZoneList[busCentroid[busId]["station"]]["lineZone"].in_count}, out={lineZoneList[busCentroid[busId]["station"]]["lineZone"].out_count}")

                                # # If >2 people come in => WAITING
                                # if in the queue ppl .... 
                                if lineZoneList[busCentroid[busId]["station"]]["lineZone"].in_count > 2:
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
                        busCentroid.pop(busId, None)

                    frame = annotatedFrame

                    # ------------------------------------ extra annotated for testing --------------------------------- #
                    # draw bounding box
                    x_min, y_min, x_max, y_max = map(int, bbox)
                    
                    # green box
                    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  

                    # display Bus ID, Status, and Station
                    text = (f"ID: {busId}, "
                            f"Status: {busCentroid[busId]['status']}, "
                            f"Station: {busCentroid[busId]['station']}")
                    cv2.putText(frame, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    # red dot for centroid
                    cv2.circle(frame, (int(centerX), int(centerY)), 5, (0, 0, 255), -1)  
            else : 
                # dont have bus 
                print("nothings")
            

            # ----------------------------------- start sending data to frontend ------------------------------------- #
            num_people = 5
            # encode frame to JPEG
            _, jpeg_frame = cv2.imencode('.jpg', frame)

            # convert to base64 to send over SSE
            b64_frame = base64.b64encode(jpeg_frame.tobytes()).decode('utf-8')

            # serialize because cant pass int or numeric value 
            sBusCentroid = serializeBusCentroid(busCentroid=busCentroid, lineZoneList=lineZoneList)

            data = {
                "frame": b64_frame,
                "num_people": 5,
                "busCentroid": sBusCentroid
            }

            yield f"data: {json.dumps(data)}\n\n"

            # sleep time 
            # time.sleep(0.05)

    # send SSE
    return StreamingHttpResponse(generate(), content_type='text/event-stream')
