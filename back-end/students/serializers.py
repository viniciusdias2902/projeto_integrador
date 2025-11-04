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


class StudentSerializer(serializers.ModelSerializer):
    monthly_payment_cents = serializers.SerializerMethodField()
    payment_day = serializers.SerializerMethodField()

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
            "payment_day",
        ]

    def get_monthly_payment_cents(self, obj):
        if obj.monthly_payment_cents is None:
            return "não informado"
        return obj.monthly_payment_cents

    def get_payment_day(self, obj):
        if obj.payment_day is None:
            return "não informado"
        return obj.payment_day


class StudentPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name", "monthly_payment_cents", "payment_day"]
        read_only_fields = ["id", "name"]

    def validate_payment_day(self, value):
        if value is not None and (value < 1 or value > 31):
            raise serializers.ValidationError("Payment day must be between 1 and 31")
        return value

    def validate_monthly_payment_cents(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Monthly payment cannot be negative")
        return value
