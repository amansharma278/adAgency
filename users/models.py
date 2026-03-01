from django.contrib.auth.models import AbstractUser
from django.db import models


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
