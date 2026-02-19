from django.db import models

from users.models import User


class AdVideo(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.FileField(upload_to='ads/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Ad(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video = models.ForeignKey(AdVideo, on_delete=models.CASCADE)
    duration = models.IntegerField()  # in seconds
    play_limit = models.IntegerField()
    priority = models.IntegerField(default=1)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
