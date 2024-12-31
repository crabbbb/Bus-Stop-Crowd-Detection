from django.urls import path
from .views import BusListView, BusDetailView, BusUtility, BusMonitor, RouteListView, RouteDetailView, RouteStationListView, RouteStationDetailView, BusStationListView, BusStationDetailView

urlpatterns = [
    path('bus/', BusListView.as_view(), name='busList'),  # Endpoint for listing/creating buses
    path('bus/<str:id>/', BusDetailView.as_view(), name='busDetail'),  # Endpoint for retrieving/updating/deleting a bus
    path('carplate/', BusUtility.as_view(), name="bus-utility"),
    path('route/', RouteListView.as_view(), name="routeList"),
    path('route/<str:id>', RouteDetailView.as_view(), name="routeDetail"),
    path('routeStation/', RouteStationListView.as_view(), name="routeStationList"),
    path('routeStation/<str:id>', RouteStationDetailView.as_view(), name="routeStationDetail"),
    path('busStation/', BusStationListView.as_view(), name="busStationList"), 
    path('busStation/<str:id>', BusStationDetailView.as_view(), name="busStationDetail"), 
    path("busMonitor/", BusMonitor, name="busMonitor"),
]