from django.urls import path
from bus_schedule.views import test_mongo_config

urlpatterns = [
    path('busSchedule/', test_mongo_config)
]
