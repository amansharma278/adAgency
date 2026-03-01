from wsgiref.validate import validator

from django.contrib.auth.models import AbstractUser
from django.db import models

from devices.models import Device


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ("SUPERADMIN", "Super Admin"),
        ("ADMIN", "Admin"),
        ("DEVICE", "Device"),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    organisation = models.CharField(max_length=255, blank=True, null=True)
    access_valid_until = models.DateTimeField(blank=True, null=True)
    access_renewal_date = models.DateTimeField(blank=True, null=True)
    device = models.ForeignKey(Device, blank=True, null=True, on_delete=models.CASCADE)

class AdGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    devices = models.ManyToManyField(Device, related_name="devices")
    def __str__(self):
        return self.name

