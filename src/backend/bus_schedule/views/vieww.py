from rest_framework.views import APIView
from django.http import StreamingHttpResponse
import time
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

def database_update_stream(request):
    def event_stream():
        while True:
            time.sleep(3)
            yield f"data: The server time is: {datetime.datetime.now()}\n\n"

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")