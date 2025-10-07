from django.db import models
from django.contrib.auth.models import User
from common.constants import SHIFT_CHOICES
from common.models import Person


class Driver(Person):
    shift = models.CharField(choices=SHIFT_CHOICES)
    dailyPaymentCents = models.IntegerField()
