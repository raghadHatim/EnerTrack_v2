from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('devices/', views.devices_view, name='devices'),
    path('dashboard/alerts/', views.alerts_view, name='alerts'),
    path('devices/add/', views.device_add_view, name='device_add'),
]