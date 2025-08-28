from rest_framework import serializers
from django.contrib.auth.models import Group, User
from .models import Driver
import re


class DriverCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Driver
        fields = ["name", "phone", "shift", "email", "password"]

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_user(username=email, email=email, password=password)

        group, created = Group.objects.get_or_create(name="drivers")
        user.groups.add(group)

        driver = Driver.objects.create(user=user, **validated_data)
        return driver

    # Validações
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


class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = ["name", "phone", "shift"]
