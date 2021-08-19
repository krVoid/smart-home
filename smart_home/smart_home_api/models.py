from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import SmallIntegerField


class Device(models.Model):
    name = models.CharField(max_length=30, unique=True)
    url = models.CharField(max_length=30, unique=True)

class DeviceInput(models.Model):
    name = models.CharField(max_length=30)
    device = models.ForeignKey(Device, related_name="deviceinput",on_delete=models.CASCADE)
    description = models.CharField(max_length=230, null = True)
    inputId = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = (("device", "name"),)  

class DeviceInputNotification(models.Model):

    class NotificationCondition(models.TextChoices):
        EQUAL = "EQUAL"
        BIGGER_OR_EQUAL = "BIGGER_OR_EQUAL"
        SMALLER_OR_EQUAL = "SMALLER_OR_EQUAL"
        SMALLER = "SMALLER"
        BIGGER = "BIGGER"

    name = models.CharField(max_length=30)
    deviceIntput = models.ForeignKey(DeviceInput, related_name="inputnotification", on_delete=models.CASCADE)
    description = models.CharField(max_length=230,blank=True, null=True)
    email = models.TextField(default='/')
    condition = models.CharField(choices=NotificationCondition.choices, default=NotificationCondition.EQUAL, max_length=50)
    threshold = models.IntegerField(default=1)
    isTurnOn = models.BooleanField(default=True)



class DeviceOutput(models.Model):
    name = models.CharField(max_length=30)
    device = models.ForeignKey(Device, related_name="deviceoutput", on_delete=models.CASCADE)
    description = models.CharField(max_length=230, null = True, blank= True)
    isBinary = models.BooleanField(default=True)
    min = models.IntegerField(blank=True, null=True)
    max = models.IntegerField(blank=True, null=True)
    outputId = models.IntegerField(blank=True, null=True)

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