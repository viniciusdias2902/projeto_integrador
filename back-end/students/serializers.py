from rest_framework import serializers
from django.contrib.auth.models import Group, User
from .models import Student
from common.serializer import PersonSerializer
import re


class StudentCreateSerializer(PersonSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = [
            "name",
            "phone",
            "class_shift",
            "university",
            "email",
            "password",
            "boarding_point",
        ]

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_user(username=email, email=email, password=password)
        group, created = Group.objects.get_or_create(name="students")
        user.groups.add(group)
        student = Student.objects.create(user=user, **validated_data)
        return student

    


class StudentSerializer(serializers.ModelSerializer):
    monthly_payment_cents = serializers.SerializerMethodField()
    last_payment_date = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "id",
            "name",
            "phone",
            "class_shift",
            "university",
            "boarding_point",
            "role",
            "monthly_payment_cents",
            "last_payment_date",
        ]

    def get_monthly_payment_cents(self, obj):
        if obj.monthly_payment_cents is None:
            return "não informado"
        return obj.monthly_payment_cents

    def get_last_payment_date(self, obj):
        if obj.last_payment_date is None:
            return "não informado"
        return obj.last_payment_date


class StudentPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name", "monthly_payment_cents", "last_payment_date"]
        read_only_fields = ["id", "name"]

    def validate_monthly_payment_cents(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Monthly payment cannot be negative")
        return value
