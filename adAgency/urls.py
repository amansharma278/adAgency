from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/ads/', include('ads.urls')),
    path('api/device/', include('devices.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
