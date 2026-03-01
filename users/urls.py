from django.urls import path

from users.views import signup, get_profile, create_group, get_groups, add_user_to_group, delete_group, \
    assign_ad_to_group

urlpatterns = [
    path('signp/', signup),
    path('profile/', get_profile),
    path('group/', get_groups),
    path('group/create/', create_group),
    path('group/delete/<int:group_id>/', delete_group),
    path('group/add-users/', add_user_to_group),
    path('group/<int:group_id>/assign-ads/', assign_ad_to_group),
]
