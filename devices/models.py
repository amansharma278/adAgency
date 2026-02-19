from django.db import models


# Create your models here.
class Device(models.Model):
    id = models.AutoField(primary_key=True)
    device_name = models.CharField(max_length=255)
    device_id = models.CharField(max_length=100, unique=True)
    secret_key = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    is_online = models.BooleanField(default=False)
    last_active = models.DateTimeField(null=True, blank=True)
    assigned_ads = models.ManyToManyField('ads.Ad', blank=True)
