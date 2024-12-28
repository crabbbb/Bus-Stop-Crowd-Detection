from django.urls import path
from .views import BusListView, BusDetailView, BusUtility, BusMonitor

urlpatterns = [
    path('bus/', BusListView.as_view(), name='busList'),  # Endpoint for listing/creating buses
    path('bus/<str:id>/', BusDetailView.as_view(), name='busDetail'),  # Endpoint for retrieving/updating/deleting a bus
    path('carplate/', BusUtility.as_view(), name="bus-utility"),
    path("busMonitor/", BusMonitor, name="busMonitor"),
]