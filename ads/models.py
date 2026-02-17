from django.db import models

# Create your models here.
class Ad(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video = models.FileField(upload_to='ads/')
    duration = models.IntegerField()  # in seconds
    play_limit = models.IntegerField()
    priority = models.IntegerField(default=1)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
