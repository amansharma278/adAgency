from django.urls import path

from devices.views import create_device, update_device, get_devices, get_device, device_login, assign_ad, \
    get_next_ad_to_play, add_in_queue, updated_playing_status, get_me, delete_device

urlpatterns = [
    path('create/', create_device),
    path('update/<int:device_id>/', update_device),
    path('<int:id>/', delete_device),
    path('', get_devices),
    path('<int:device_id>/', get_device),
    path('me/', get_me),
    path('<int:device_id>/assign-ad/', assign_ad),
    path('<int:device_id>/next-ad/', get_next_ad_to_play),
    path('<int:device_id>/add-in-queue/', add_in_queue),
    path('<int:device_id>/update-playing-status/', updated_playing_status),
    path('login/', device_login),
]
