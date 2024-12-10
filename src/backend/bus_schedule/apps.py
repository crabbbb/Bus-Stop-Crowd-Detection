from django.apps import AppConfig
from backend.utils import setup

class BusScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bus_schedule'

    # def ready(self) : 
    #     # the action here will be automoated run after the app is ready 
    #     # setup()
