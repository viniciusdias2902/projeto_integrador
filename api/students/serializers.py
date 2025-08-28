from rest_framework import serializers
from django.contrib.auth.models import Group, User
from .models import Student


class StudentCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ["name", "phone", "class_shift", "university", "email", "password"]

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_user(username=email, email=email, password=password)
        group, created = Group.objects.get_or_create(name="students")
        user.groups.add(group)
        student = Student.objects.create(user=user, **validated_data)
        return student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["name", "phone", "class_shift", "university"]
