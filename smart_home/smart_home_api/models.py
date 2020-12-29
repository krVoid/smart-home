from django.db import models
from django.contrib.auth.models import AbstractUser


class Device(models.Model):
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=30)
