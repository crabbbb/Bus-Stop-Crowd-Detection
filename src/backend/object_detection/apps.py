from django.apps import AppConfig
from threading import Thread
import time

class ObjectDetectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'object_detection'

    # def ready(self):
    #     from .views import videoProcess

    #     # Run the video processing task in a separate thread
    #     thread = Thread(target=videoProcess, daemon=True)
    #     thread.start()
