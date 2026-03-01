from rest_framework import serializers

from devices.serializers import DeviceSerializer
from users.models import User, AdGroup


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','is_staff','is_active','date_joined')

class AdGroupSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(many=True)
    class Meta:
        model = AdGroup
        fields = '__all__'

