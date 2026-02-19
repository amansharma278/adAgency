from django.urls import path

from ads.views import upload_video, create_ad, update_ad, get_ad, get_ads

urlpatterns = [
    path('video/upload/', upload_video),
    path('create/', create_ad),
    path('update/<int:ad_id>/', update_ad),
    path('', get_ads),
    path('<int:ad_id>/', get_ad),
]
