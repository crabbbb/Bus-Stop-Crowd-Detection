from django.urls import path
from .views import BusListView, BusDetailView

urlpatterns = [
    path('buses/', BusListView.as_view(), name='bus-list'),  # Endpoint for listing/creating buses
    path('buses/<str:pk>/', BusDetailView.as_view(), name='bus-detail'),  # Endpoint for retrieving/updating/deleting a bus
]