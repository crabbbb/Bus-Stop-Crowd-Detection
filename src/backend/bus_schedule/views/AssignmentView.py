from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Assignment, Route, Bus
from ..serializer import AssignmentSerializer
from backend.utils import message
from datetime import datetime, timedelta

# no need id to create 
class AssignmentListView(APIView) : 
    # get all 
    def get(self, request) :
        print("Get Function active ")
        print("Query Params:", request.query_params)

        # if have request filter it 
        assignmentId = request.query_params.get("AssignmentId")
        minTime = request.query_params.get("Time")
        maxTime = request.query_params.get("Time")
        dayOfWeek = request.query_params.get("DayOfWeek")
        busId = request.query_params.get("BusId")
        routeId = request.query_params.get("RouteId")

        filters = []

        if assignmentId:
            filters.append({"AssignmentId": {"$regex": assignmentId, "$options": "i"}})
        if minTime:
            filters.append({"Time": {"$gte": datetime.strptime(minTime, "%H:%M:%S")}})
        if maxTime : 
            filters.append({"Time": {"$lte": datetime.strptime(maxTime, "%H:%M:%S")}})
        if dayOfWeek:
            filters.append({"DayOfWeek": {"$eq": int(dayOfWeek)}})
        if busId:
            filters.append({"BusId": {"$regex": busId, "$options": "i"}})
        if routeId:
            filters.append({"RouteId": {"$regex": routeId, "$options": "i"}})

        query = {"$and": filters} if filters else {}
        
        # get data 
        try : 
            assignment = Assignment()
            assignments = None
            
            # fill in data to buss
            if not query : 
                # filter is empty
                assignments = assignment.getAll()
            else :
                # filter not empty 
                assignments = assignment.getByfilter(query)
            
            if assignments is None : 
                # file problem
                return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif not assignments : 
                # empty list , database dont have data 
                return Response({"message": message.NOT_FOUND}, status=status.HTTP_200_OK)

            # have data 
            serializer = AssignmentSerializer(assignments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ConnectionError as e :
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            # 1. Parse request data
            time_str = request.data.get("Time", None)
            day_of_week = request.data.get("DayOfWeek", None)
            bus_id = request.data.get("BusId", None)
            route_id = request.data.get("RouteId", None)
            
            # Basic validation
            if not time_str or not day_of_week or not bus_id or not route_id:
                return Response(
                    {"error": "Time, DayOfWeek, BusId, and RouteId are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Convert time_str "HH:MM:SS" to datetime.time or keep as string
            # If you store times as string in DB, you can keep them as is
            # but let's parse to datetime to do overlap logic
            try:
                time_obj = datetime.strptime(time_str, "%H:%M:%S")
            except ValueError:
                return Response(
                    {"error": "Invalid time format. Must be HH:MM:SS."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 2. Check if BusId actually exists
            bus_model = Bus()  # or whatever your Bus model is
            bus_data = bus_model.getWithID(bus_id)
            if not bus_data:
                return Response(
                    {"error": f"BusId '{bus_id}' not found in Bus collection."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 3. Check if RouteId actually exists
            route_model = Route()
            route_data = route_model.getWithID(route_id)
            if not route_data:
                return Response(
                    {"error": f"RouteId '{route_id}' not found in Route collection."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Assume route_data has a "RouteDuration" in minutes
            route_duration_minutes = route_data.get("RouteDuration", 0)
            if not isinstance(route_duration_minutes, int):
                route_duration_minutes = int(route_duration_minutes or 0)
            
            # 4. Check for exact duplicates of (Time, DayOfWeek, BusId, RouteId)
            assignment_model = Assignment()
            duplicate_filter = {
                "Time": time_obj.strftime("%H:%M:%S"),  # or keep as string
                "DayOfWeek": int(day_of_week),
                "BusId": bus_id,
                "RouteId": route_id
            }
            
            # Use $and if you prefer, but a direct filter is also fine
            existing_duplicates = assignment_model.getByfilter(duplicate_filter)
            if existing_duplicates:
                return Response(
                    {"error": "Duplicate assignment with same Time, DayOfWeek, BusId, RouteId already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 5. Check bus availability: no overlap in time range
            #    Overlap means an existing assignment for the same bus that
            #    would conflict with [time_obj, time_obj + route_duration].
            
            # We define a conflict if the new assignment's start time is between an existing assignment's 
            # time range, or vice versa. We'll check all assignments for same BusId and DayOfWeek
            conflict_filter = {
                "BusId": bus_id,
                "DayOfWeek": int(day_of_week)
            }
            existing_assignments = assignment_model.getByfilter(conflict_filter)
            
            new_start = time_obj
            new_end = time_obj + timedelta(minutes=route_duration_minutes)
            
            for item in existing_assignments:
                existing_time_str = item.get("Time", "")
                try:
                    existing_time_obj = datetime.strptime(existing_time_str, "%H:%M:%S")
                except ValueError:
                    # skip if it can't parse
                    continue
                
                # get existing route duration
                existing_route_id = item.get("RouteId", None)
                existing_route_data = route_model.getWithID(existing_route_id)
                existing_duration = existing_route_data.get("RouteDuration", 0) if existing_route_data else 0
                if not isinstance(existing_duration, int):
                    existing_duration = int(existing_duration or 0)
                
                existing_start = existing_time_obj
                existing_end = existing_time_obj + timedelta(minutes=existing_duration)
                
                # check overlap
                # overlap if new_start < existing_end and existing_start < new_end
                if new_start < existing_end and existing_start < new_end:
                    return Response(
                        {
                            "error": f"Time conflict > bus {bus_id} is already assigned from {existing_start.strftime('%H:%M:%S')} to {existing_end.strftime('%H:%M:%S')}"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # 6. Passed all checks -> create assignment
            #    You can decide to store times as string or keep them as datetime.
            #    We'll store as string HH:MM:SS for consistency with your existing data.
            data_to_insert = {
                "Time": time_obj.strftime("%H:%M:%S"),
                "DayOfWeek": int(day_of_week),
                "BusId": bus_id,
                "RouteId": route_id
            }
            
            result = assignment_model.createOne(data_to_insert)
            if not result:
                return Response(
                    {"error": message.CONFIGURATION_ERROR},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # If inserted successfully, return the newly created document
            new_assignment = assignment_model.getWithID(data_to_insert["AssignmentId"])
            serializer = AssignmentSerializer(new_assignment, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except ConnectionError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AssignmentDetailView(APIView) :
    def get(self, request, id) : 
        try :
            if id : 
                # have data
                assignment = Assignment()

                # get the class 
                result = assignment.getWithID(id)

                # check None
                if result is None : 
                    return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # check empty 
                if not result : 
                    # 404 page not found 
                    return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
                
                # have data 
                serializer = AssignmentSerializer(result)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else : 
                # dont have 
                return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        except ConnectionError as e : 
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # update 
    def put(self, request, id):
        """
        Update an existing Assignment with ID == id.
        Steps:
        1) Validate existence of the assignment.
        2) Parse & validate incoming fields.
        3) Check duplicates (Time, DayOfWeek, BusId, RouteId), excluding self.
        4) Check bus-time overlap, excluding self.
        5) Update the record if all checks pass.
        """
        try:
            # 1) Retrieve existing assignment by ID
            assignment_model = Assignment()
            existing_assignment = assignment_model.getWithID(id)
            if not existing_assignment:
                # If None or empty, no record found
                return Response({"error": f"AssignmentId '{id}' not found."},
                                status=status.HTTP_404_NOT_FOUND)

            # 2) Parse request data
            time_str = request.data.get("Time", None)
            day_of_week = request.data.get("DayOfWeek", None)
            bus_id = request.data.get("BusId", None)
            route_id = request.data.get("RouteId", None)

            # Basic validation
            if not time_str or not day_of_week or not bus_id or not route_id:
                return Response(
                    {"error": "Time, DayOfWeek, BusId, and RouteId are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Convert Time to a datetime object (or keep as string if you prefer)
            try:
                time_obj = datetime.strptime(time_str, "%H:%M:%S")
            except ValueError:
                return Response(
                    {"error": "Invalid time format. Must be HH:MM:SS."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2b) Check Bus existence
            bus_model = Bus()
            bus_data = bus_model.getWithID(bus_id)
            if not bus_data:
                return Response(
                    {"error": f"BusId '{bus_id}' not found in Bus collection."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 2c) Check Route existence
            route_model = Route()
            route_data = route_model.getWithID(route_id)
            if not route_data:
                return Response(
                    {"error": f"RouteId '{route_id}' not found in Route collection."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            route_duration_minutes = route_data.get("RouteDuration", 0)
            if not isinstance(route_duration_minutes, int):
                route_duration_minutes = int(route_duration_minutes or 0)

            # 3) Check for exact duplicates of (Time, DayOfWeek, BusId, RouteId)
            duplicate_filter = {
                "Time": time_obj.strftime("%H:%M:%S"),
                "DayOfWeek": int(day_of_week),
                "BusId": bus_id,
                "RouteId": route_id
            }
            duplicates = assignment_model.getByfilter(duplicate_filter)
            # If we find duplicates, ensure it's not the same record
            for dup in duplicates:
                if dup.get("AssignmentId") != existing_assignment.get("AssignmentId"):
                    return Response(
                        {"error": "Another assignment with the same (Time, DayOfWeek, BusId, RouteId) already exists."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # 4) Check bus availability (no overlap) excluding this record
            conflict_filter = {
                "BusId": bus_id,
                "DayOfWeek": int(day_of_week)
            }
            existing_assignments = assignment_model.getByfilter(conflict_filter)

            new_start = time_obj
            new_end = time_obj + timedelta(minutes=route_duration_minutes)

            for item in existing_assignments:
                # skip the same record
                if item.get("AssignmentId") == existing_assignment.get("AssignmentId"):
                    continue

                existing_time_str = item.get("Time", "")
                try:
                    existing_time_obj = datetime.strptime(existing_time_str, "%H:%M:%S")
                except ValueError:
                    continue
                
                existing_route_id = item.get("RouteId", None)
                existing_route_data = route_model.getWithID(existing_route_id)
                existing_duration = existing_route_data.get("RouteDuration", 0) if existing_route_data else 0
                if not isinstance(existing_duration, int):
                    existing_duration = int(existing_duration or 0)
                
                existing_start = existing_time_obj
                existing_end = existing_time_obj + timedelta(minutes=existing_duration)

                # Overlap check
                if new_start < existing_end and existing_start < new_end:
                    return Response(
                        {
                            "error": f"Time conflict: bus {bus_id} is already assigned from {existing_start.strftime('%H:%M:%S')} to {existing_end.strftime('%H:%M:%S')}"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # 5) Passed all checks -> update assignment
            updated_data = {
                "AssignmentId": existing_assignment["AssignmentId"],
                "Time": time_obj.strftime("%H:%M:%S"),
                "DayOfWeek": int(day_of_week),
                "BusId": bus_id,
                "RouteId": route_id
            }
            update_result = assignment_model.updateOne(updated_data)
            if not update_result:
                return Response({"error": "Could not update the record."}, status=status.HTTP_404_NOT_FOUND)

            # 6) Return updated record
            updated_assignment = assignment_model.getWithID(existing_assignment["AssignmentId"])
            serializer = AssignmentSerializer(updated_assignment, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ConnectionError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id) : 
        print("Delete function archieve")
        try : 
            if id : 
                assignment = Assignment()

                # get the data 
                result = assignment.getWithID(id)

                # check None
                if result is None : 
                    return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # check empty 
                if not result : 
                    # 404 page not found 
                    return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
                
                # have data 
                # perform delete 
                assignment.deleteOne(idData=id)
                return Response(
                    {
                        "success": f"{message.DELETE_SUCCESS}, ID : {result["AssignmentId"]}",
                        "redirect": BusUtility.getHomePage(result["AssignmentId"])
                    }, 
                    status=status.HTTP_200_OK
                )
            else : 
                # dont have 
                return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        except ConnectionError as e : 
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BusUtility(APIView) :
    @staticmethod
    def getHomePage(id : str) :
        return f"/assignment?id={id}"
    
    @staticmethod
    def getDetailPage(id : str) :
        return f"/assignment/detail/{id}"