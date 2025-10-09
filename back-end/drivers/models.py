from django.db import models
from django.contrib.auth.models import User, Group
from common.constants import SHIFT_CHOICES

from common.models import Person


class Driver(Person):
    shift = models.CharField(choices=SHIFT_CHOICES)
    dailyPaymentCents = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.role:
            self.role = "driver"
        super().save(*args, **kwargs)
        if self.user:
            group, _ = Group.objects.get_or_create(name="drivers")
            self.user.groups.add(group)
