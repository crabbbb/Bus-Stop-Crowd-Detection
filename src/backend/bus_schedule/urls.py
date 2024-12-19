from django.urls import path
from .views import BusListView, BusUtility

urlpatterns = [
    path('bus/', BusListView.as_view(), name='busList'),  # Endpoint for listing/creating buses
    # path('bus/<str:id>/', BusDetailView.as_view(), name='busDetail'),  # Endpoint for retrieving/updating/deleting a bus
    path('bus/carplate/', BusUtility.as_view(), name="bus-utility"),
]