from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from analytics.models import PlayLog
from analytics.serializers import PlayLogSerializer


# Create your views here.

@api_view(['GET'])
def get_playlogs(request):
    playlogs = PlayLog.objects.all()
    serializer = PlayLogSerializer(playlogs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_playlog(request, playlog_id):
    playlog = PlayLog.objects.get(id=playlog_id)
    serializer = PlayLogSerializer(playlog)
    return Response(serializer.data, status=status.HTTP_200_OK)
