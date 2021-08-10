from django.db import models
from django.contrib.auth.models import AbstractUser


class Device(models.Model):
    name = models.CharField(max_length=30, unique=True)
    url = models.CharField(max_length=30, unique=True)


class DeviceInput(models.Model):
    name = models.CharField(max_length=30)
    device = models.ForeignKey(Device, related_name="deviceinput",on_delete=models.CASCADE)
    description = models.CharField(max_length=230, null = True)

    class Meta:
        unique_together = (("device", "name"),)  


class DeviceOutput(models.Model):
    name = models.CharField(max_length=30)
    device = models.ForeignKey(Device, related_name="deviceoutput", on_delete=models.CASCADE)
    description = models.CharField(max_length=230, null = True)
    isBinary = models.BooleanField(default=True)
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=1)
    class Meta:
        unique_together = (("device", "name"),)  


class DeviceOutputAction(models.Model):

    class ActionType(models.TextChoices):
        POST = 'POST'
        GET = 'GET'

    name = models.CharField(max_length=30)
    deviceOutput = models.ForeignKey(DeviceOutput, related_name="outputaction", on_delete=models.CASCADE)
    description = models.CharField(max_length=230, null = True)
    url = models.TextField(default='/')
    type = models.CharField(choices=ActionType.choices, default=ActionType.GET, max_length=50)
    parameters = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = (("deviceOutput", "name"),)  