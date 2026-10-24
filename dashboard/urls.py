from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.devices_view, name='devices'),
    path('devices/add/', views.device_add_view, name='device_add'),
]