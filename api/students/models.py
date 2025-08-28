from django.db import models
from django.contrib.auth.models import User
from common.constants import SHIFT_CHOICES
from common.models import Person

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
