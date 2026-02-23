from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from tinytag import TinyTag

from ads.models import AdVideo, Ad
from ads.serializers import AdVideoSerializer, AdSerializer


# Create your views here.
@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_video(request):
    data = request.FILES
    serializer = AdVideoSerializer(data=data)
    if serializer.is_valid():
        serializer.save(uploaded_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_ad(request):
    serializer = AdSerializer(data=request.data)
    if serializer.is_valid():
        model = serializer.save(created_by=request.user)
        try:
            tag = TinyTag.get(model.video.video.path)
            model.duration = int(tag.duration)
            model.save()
        except Exception as e:
            print(e)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_ad(request, ad_id):
    ad_object = Ad.objects.get(id=ad_id)
    serializer = AdSerializer(ad_object, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_ads(request):
    devices = Ad.objects.all()
    serializer = AdSerializer(devices, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_ad(request, ad_id):
    device = Ad.objects.get(id=ad_id)
    serializer = AdSerializer(device)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_ad(request, ad_id):
    ads_object = Ad.objects.filter(id=ad_id).first()
    # Ye jo ads id aayee hai usko Db ke ads id se match kerao
    if ads_object:
        ads_object.delete()
        return Response({"message":"Ads successfully deleted."}, status=status.HTTP_200_OK)
    else:
        return Response({"message":"Ads not found."}, status=status.HTTP_404_NOT_FOUND)






