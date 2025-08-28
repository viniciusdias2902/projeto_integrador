from django.db import models
from django.contrib.auth.models import User
from constants import SHIFT_CHOICES


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=11)
    shift = models.CharField(choices=SHIFT_CHOICES)
