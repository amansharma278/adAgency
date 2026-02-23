from datetime import datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ads.models import Ad
from ads.serializers import AdSerializer
from analytics.models import PlayLog
from analytics.serializers import PlayLogSerializer
from devices.helper import create_device_access_token, create_device_refresh_token
from devices.models import Device
from devices.serializers import DeviceSerializer
from users.models import User


# Create your views here.
@api_view(['POST'])
def create_device(request):
    serializer = DeviceSerializer(data=request.data)
    if serializer.is_valid():
        device = serializer.save()
        user = User(username=device.device_id)
        user.set_password(device.secret_key)
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_device(request, device_id):
    device_object = Device.objects.get(id=device_id)
    serializer = DeviceSerializer(device_object, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_devices(request):
    devices = Device.objects.all()
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_device(request, device_id):
    device = Device.objects.get(id=device_id)
    serializer = DeviceSerializer(device)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_me(request):
    device_user = request.user
    device = Device.objects.filter(device_id=device_user.username).first()
    serializer = DeviceSerializer(device)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def device_login(request):
    data = request.data
    device_id = data.get('device_id')
    device_secret = data.get('device_secret')
    if device_id and device_secret:
        device = Device.objects.filter(device_id=device_id, secret_key=device_secret).first()
        if device:
            access_token = create_device_access_token(device)
            refresh_token = create_device_refresh_token(device)
            return Response({"access": access_token, "refresh": refresh_token}, status=status.HTTP_200_OK)
        else:
            Response({"message": "Provided details are invalid!"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        Response({"message": "Device Id and Device secret is required."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def assign_ad(request, device_id):
    device_object = Device.objects.get(id=device_id)
    if device_object:
        ad_ids = request.data.get('ads')
        if ad_ids:
            ads = Ad.objects.filter(id__in=ad_ids).all()
            device_object.assigned_ads.set(ads)
            device_object.save()
            return Response(DeviceSerializer(device_object).data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Ads is/are required."}, status=status.HTTP_400_BAD_REQUEST)

    else:
        Response({"message": "Device Id and Device secret is required."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_next_ad_to_play(request, device_id):
    device_object = Device.objects.get(id=device_id)
    if device_object:
        if device_object.assigned_ads.count() == 0:
            return Response({"message": "Ads is/are not assigned."}, status=status.HTTP_400_BAD_REQUEST)
        playlog = PlayLog.objects.order_by('-id').first()
        if playlog:
            try:
                playing_ad_position = [ad.id for ad in device_object.assigned_ads.all()].index(playlog.ad.id)
                # ad = Ad.objects.get(
                #     id=device_object.assigned_ads.all()[(playing_ad_position + 1) % device_object.assigned_ads.count()])
                ad = device_object.assigned_ads.all()[(playing_ad_position + 1) % device_object.assigned_ads.count()]
                serializer = AdSerializer(ad)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                # ad = Ad.objects.get(id=device_object.assigned_ads.all()[0])
                serializer = AdSerializer(device_object.assigned_ads.first())
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # ad = Ad.objects.get(id=device_object.assigned_ads.all()[0])
            serializer = AdSerializer(device_object.assigned_ads.first())
            return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        Response({"message": "Device Id and Device secret is required."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_in_queue(request, device_id):
    serializer = PlayLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def updated_playing_status(request, device_id):
    data = request.data
    playlog_id = data.get('id')
    if playlog_id:
        playlog = PlayLog.objects.get(id=playlog_id)
        serializer = PlayLogSerializer(playlog, data=data, partial=True)
        if serializer.is_valid():
            if data.get('status') == 'Started':
                serializer.save(updated_at=datetime.now(), started_at=datetime.now())
            elif data.get('status') == 'Completed':
                serializer.save(updated_at=datetime.now(), finished_at=datetime.now())
            else:
                serializer.save(updated_at=datetime.now())
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Enter valid playlog id!"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "Playlog id is required!"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_device(request, id):
    device_object = Device.objects.filter(id=id).first()

    if device_object:
        user = User.objects.filter(username=device_object.device_id).first()
        device_object.delete()
        user.delete()
        return Response({"message":"Device successfully deleted."}, status=status.HTTP_200_OK)
    else:
        return Response({"message":"Device does not found!"}, status=status.HTTP_400_BAD_REQUEST)
