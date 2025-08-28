from django.db import models
from django.contrib.auth.models import User
from constants import SHIFT_CHOICES

UNIVERSITY_CHOICES = (
    ("UESPI", "Universidade Estadual do Piauí"),
    ("CHRISFAPI", "Christus Faculdade do Piauí"),
    ("IFPI", "Instituto Federal do Piauí"),
    ("ETC", "Outro"),
)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    phone = models.CharField(max_length=11, null=False, blank=False)
    registration_date = models.DateField(auto_now_add=True)
    class_shift = models.CharField(choices=SHIFT_CHOICES, blank=False, null=False)
    university = models.CharField(choices=UNIVERSITY_CHOICES)
