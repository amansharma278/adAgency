from rest_framework import serializers

from devices.models import Device
from devices.serializers import DeviceSerializer
from .models import Ad, AdVideo


class AdVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdVideo
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'uploaded_at']


class AdSerializer(serializers.ModelSerializer):
    video_url = serializers.SerializerMethodField()
    devices = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']

    def get_video_url(self, obj):
        return obj.video.video.name


    def get_devices(self, obj):
        return obj.devices.values_list('id', flat=True)
