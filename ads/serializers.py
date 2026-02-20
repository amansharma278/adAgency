from rest_framework import serializers
from .models import Ad, AdVideo


class AdSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']

    def get_video(self, obj):
        return obj.video.video.name


class AdVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdVideo
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'uploaded_at']
