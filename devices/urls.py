from django.urls import path

from devices.views import create_device, update_device, get_devices, get_device, device_login

urlpatterns = [
    path('create/', create_device),
    path('update/<int:device_id>/', update_device),
    path('', get_devices),
    path('<int:device_id>/', get_device),
    path('login/', device_login),
]
