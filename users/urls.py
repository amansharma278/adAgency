from django.urls import path

from users.views import signup, get_profile

urlpatterns = [
    path('signp/', signup),
    path('profile/', get_profile)
]
