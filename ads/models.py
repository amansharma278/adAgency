import os
import subprocess

from decouple import config
from django.core.files.base import ContentFile
from django.db import models
from tinytag import TinyTag

from users.models import User


class AdVideo(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.FileField(upload_to='ads/')
    thumbnail = models.ImageField(upload_to='ads/thumbs/', blank=True, null=True)
    duration = models.IntegerField(null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.video and not self.duration:
            video_path = self.video.path
            thumb_path = video_path[:-4] + "_thumb.jpg"
            print(video_path)
            print(thumb_path)

            self.duration = int(TinyTag.get(video_path).duration)
            ffmpeg_exe = f'{config("FFMPEG_PATH")}'
            cmd = [ffmpeg_exe, '-y', '-i', video_path, '-ss', '1', '-vframes', '1', thumb_path]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            if os.path.exists(thumb_path):
                with open(thumb_path, 'rb') as f:
                    self.thumbnail.save(os.path.basename(thumb_path), ContentFile(f.read()), save=False)
                os.remove(thumb_path)  # Clean up temp file

            super().save(update_fields=['duration', 'thumbnail'])


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
