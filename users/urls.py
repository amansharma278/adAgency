from django.urls import path

from users.views import signup, get_profile, create_group, get_groups, add_user_to_group

urlpatterns = [
    path('signp/', signup),
    path('profile/', get_profile),
    path('group/', create_group),
    path('group/', get_groups),
    path('group/add-users/', add_user_to_group),
]
