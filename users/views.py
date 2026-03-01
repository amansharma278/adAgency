from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.auth import is_admin
from users.models import User
from users.serializer import UserSerializer


# Create your views here.
def signup(request):
    email = request.POST['email']
    password = request.POST['password']
    if email:
        return JsonResponse({
            "message": "Please enter your email address",
            "success": False,
        })
    user = User.objects.filter(email=email)
    if user:
        User.objects.create_user(email, password)
        return JsonResponse({
            "message": "Successfully created user",
            "success": True,
        })
    else:
        return JsonResponse({
            "message": "Something went wrong",
        })


def profile(request):
    user = request.user
    return JsonResponse({
        "user": UserSerializer(user).data,
    })


@api_view(['GET'])
def get_profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@login_required
@api_view(['POST'])
def create_group(request):
    user = request.user
    group_name = request.data.get('group_name')
    if not group_name:
        return Response({"error": "Group name is required"}, status=status.HTTP_400_BAD_REQUEST)
    if user.role != "ADMIN":
        return Response({"error": "Insufficient Permission"}, status=status.HTTP_403_FORBIDDEN)

    Group.objects.create(name=f"{user.organisation}_{group_name}", created_by=request.user)

    return Response({"message": f"Group '{group_name}' created successfully"}, status=status.HTTP_201_CREATED)


@user_passes_test(is_admin)
@login_required
@api_view(['GET'])
def get_groups(request):
    user = request.user

    groups = Group.objects.filter(name__startswith=f"{user.organisation}_")
    return Response({"groups": groups}, status=status.HTTP_200_OK)


@user_passes_test(is_admin)
@login_required
@api_view(['POST'])
def add_user_to_group(request):
    user = request.user
    group_id = request.data.get('group_id')
    user_ids = request.data.get('user_ids', [])

    if not group_id:
        return Response({"error": "Group id is required!"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        group = Group.objects.get(id=group_id, name__startswith=f"{user.organisation}_")
        user_to_add = User.objects.get(id__in=user_ids, organisation=user.organisation, role="DEVICE")
        group.user_set.add(user_to_add)
        return Response({"message": f"Users added to group '{group.name}' successfully"},
                        status=status.HTTP_200_OK)
    except Group.DoesNotExist:
        return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
