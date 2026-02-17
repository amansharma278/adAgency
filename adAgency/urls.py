from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import profile

# from ads.views import VideoAdViewSet
# from devices.views import DeviceViewSet
# from schedule.views import AdScheduleViewSet

router = DefaultRouter()
# router.register(r'videos', VideoAdViewSet)
# router.register(r'devices', DeviceViewSet)
# router.register(r'schedules', AdScheduleViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/',include('rest_framework.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', profile),
]
