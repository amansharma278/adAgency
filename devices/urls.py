from django.urls import path

from devices.views import create_device, update_device, get_devices, get_device, device_login, assign_ad, \
    get_next_ad_to_play

urlpatterns = [
    path('create/', create_device),
    path('update/<int:device_id>/', update_device),
    path('', get_devices),
    path('<int:device_id>/', get_device),
    path('<int:device_id>/assign-ad/', assign_ad),
    path('<int:device_id>/next-ad/', get_next_ad_to_play),
    path('login/', device_login),
]
