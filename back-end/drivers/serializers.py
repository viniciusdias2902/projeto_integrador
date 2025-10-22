from rest_framework import serializers
from django.contrib.auth.models import Group, User
from .models import Driver
from common.serializer import PersonSerializer


class DriverCreateSerializer(PersonSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    dailyPaymentCents = serializers.IntegerField(required=False, default=0)

    class Meta:
        model = Driver
        fields = [
            "name",
            "phone",
            "shift",
            "email",
            "password",
            "dailyPaymentCents",
        ]

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_user(username=email, email=email, password=password)

        group, created = Group.objects.get_or_create(name="drivers")
        user.groups.add(group)

        driver = Driver.objects.create(user=user, **validated_data)
        return driver


class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = ["name", "phone", "shift", "role", "dailyPaymentCents"]
