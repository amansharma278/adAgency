from django.db import models


# Create your models here.
class PlayLog(models.Model):
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE)
    ad = models.ForeignKey('ads.Ad', on_delete=models.CASCADE)
    started_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default='Playing')
    finished_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
