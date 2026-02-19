from django.urls import path

from analytics.views import get_playlogs, get_playlog

urlpatterns = [
    path('', get_playlogs),
    path('<int:playlog_id>/', get_playlog),
]
