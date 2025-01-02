from django.urls import path
from .views import videoProcess

urlpatterns = [
    path('stream/', videoProcess, name='streamVideo'),
]