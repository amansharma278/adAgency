from rest_framework import serializers
from .models import Ad, AdVideo


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']


class AdVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdVideo
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'uploaded_at']
