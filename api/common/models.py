from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=11)

    class Meta:
        abstract = True

class BoardingPoint(models.Model):
    name = models.CharField(max_length=255, help_text="Ex: Praça Central, Posto Shell")
    address_reference = models.CharField(max_length=255, blank=True, null=True, help_text="Ex: Em frente à farmácia")
    route_order = models.PositiveIntegerField(default=0, help_text="Ordem em que o motorista passa no ponto (0, 1, 2...)")

    class Meta:
        ordering = ['route_order']

    def __str__(self):
        return f"{self.route_order}: {self.name}"