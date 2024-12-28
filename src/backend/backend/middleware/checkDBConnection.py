from django.http import JsonResponse
from backend.utils import mongo

class CheckDBConnectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Check if the MongoDB connection is healthy using the `MongoDB` class
            if not mongo.isHealthy():
                # Attempt to reconnect if the connection is not healthy
                result = mongo.reconnect()
        except Exception as e:
            # If the database cannot reconnect, return an error response
            return JsonResponse({"error": "Database connection error", "details": str(e)}, status=500)

        # Proceed with the normal response if the database connection is healthy
        return self.get_response(request)