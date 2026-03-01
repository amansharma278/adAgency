from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ads.models import Ad
from devices.models import Device
from users.auth import is_admin
from users.models import User, AdGroup
from users.serializer import UserSerializer, AdGroupSerializer


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


@api_view(['POST'])
def create_group(request):
    user = request.user
    group_name = request.data.get('name')
    device_ids = request.data.get('device_ids')
    devices = Device.objects.filter(id__in=device_ids)
    if not group_name:
        return Response({"error": "Group name is required"}, status=status.HTTP_400_BAD_REQUEST)
    if user.role != "Admin":
        return Response({"error": "Insufficient Permission"}, status=status.HTTP_403_FORBIDDEN)

    ad_group = AdGroup.objects.create(name=group_name, created_by=request.user)
    ad_group.devices.add(*devices)

    return Response({"message": f"Group '{group_name}' created successfully"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_groups(request):
    user = request.user

    ad_groups = AdGroup.objects.filter(created_by=user).all()
    serializer = AdGroupSerializer(ad_groups, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
def add_user_to_group(request):
    user = request.user
    group_id = request.data.get('group_id')
    user_ids = request.data.get('user_ids', [])

    if not group_id:
        return Response({"error": "Group id is required!"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ad_group = AdGroup.objects.get(id=group_id, created_by=user)
        user_to_add = User.objects.get(id__in=user_ids, role="DEVICE")
        ad_group.members.add(user_to_add)
        return Response({"message": f"Users added to group '{ad_group.name}' successfully"},
                        status=status.HTTP_200_OK)
    except Group.DoesNotExist:
        return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_group(request, group_id):
    group = AdGroup.objects.get(id=group_id)
    if not group:
        return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
    group.delete()
    return Response({"message": f"Group deleted successfully"})

@api_view(['POST'])
def assign_ad_to_group(request, group_id):
    ad_group = AdGroup.objects.get(id=group_id)
    if ad_group:
        ad_ids = request.data.get('ad_ids')
        if ad_ids:
            ads = Ad.objects.filter(id__in=ad_ids).all()
            for device in ad_group.devices.all():
                device.assigned_ads.add(*ads)
                device.save()
            return Response({"message":"Ads are assigned to group."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Ads is/are required."}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"message": "Not a valid Group"}, status=status.HTTP_400_BAD_REQUEST)
