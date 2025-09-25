from rest_framework import serializers
import re
from django.contrib.auth.models import User
from .models import BoardingPoint


class PersonSerializer(serializers.ModelSerializer):

    def validate_phone(self, value):
        if not re.fullmatch(r"\d{10,11}", value):
            raise serializers.ValidationError(
                "Phone number must contain 10 or 11 digits"
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long"
            )
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "Password must contain at least one number"
            )
        if not re.search(r"[A-Za-z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one letter"
            )
        return value

class BoardingPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardingPoint
        fields = ['id', 'name', 'address_reference', 'route_order']