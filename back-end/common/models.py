from django.db import models
from django.contrib.auth.models import User


ROLE_CHOICES = (
    ("student", "Student"),
    ("employee", "Employee"),
    ("admin", "Administrator"),
)


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=11)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        abstract = True
