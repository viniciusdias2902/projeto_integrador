from django.db import models
from django.contrib.auth.models import User
from common.constants import SHIFT_CHOICES
from common.models import Person
from boarding_points.models import BoardingPoint

UNIVERSITY_CHOICES = (
    ("UESPI", "Universidade Estadual do Piauí"),
    ("CHRISFAPI", "Christus Faculdade do Piauí"),
    ("IFPI", "Instituto Federal do Piauí"),
    ("ETC", "Outro"),
)


class Student(Person):
    registration_date = models.DateField(auto_now_add=True)
    class_shift = models.CharField(choices=SHIFT_CHOICES, blank=False, null=False)
    university = models.CharField(choices=UNIVERSITY_CHOICES)

    boarding_point = models.ForeignKey(
        BoardingPoint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )

    monthly_payment_cents = models.IntegerField(null=True, blank=True)
    payment_day = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.role:
            self.role = "student"
        super().save(*args, **kwargs)
