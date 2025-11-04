from rest_framework import serializers
from django.contrib.auth.models import Group, User
from .models import Admin
from common.serializer import PersonSerializer


class AdminCreateSerializer(PersonSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Admin
        fields = [
            "name",
            "phone",
            "email",
            "password",
        ]

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_superuser(
            username=email, email=email, password=password
        )

        group, created = Group.objects.get_or_create(name="admins")
        user.groups.add(group)

        admin = Admin.objects.create(user=user, **validated_data)
        return admin


class AdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Admin
        fields = ["id", "name", "phone", "role", "email"]
        read_only_fields = ["id", "role"]
