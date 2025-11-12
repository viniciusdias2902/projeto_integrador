from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.exceptions import ValidationError
from unittest.mock import Mock, patch
from datetime import date
from django.http import HttpRequest

from students.serializers import (
    StudentCreateSerializer,
    StudentSerializer,
    StudentPaymentSerializer,
)
from students.views import (
    StudentPaymentListView,
    StudentPaymentBulkUpdateView,
)
from students.models import Student
from common.permissions import GlobalDefaultPermission
from boarding_points.models import BoardingPoint


# Tabela 1
class StudentCreateSerializerValidationTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="existente@email.com",
            email="existente@email.com",
            password="Password123",
        )
        cls.boarding_point = BoardingPoint.objects.create(
            name="Ponto Teste", route_order=1
        )

        cls.valid_data = {
            "name": "Aluno Teste",
            "phone": "86999887766",
            "class_shift": "M",
            "university": "UESPI",
            "email": "novo@email.com",
            "password": "Password123",
            "boarding_point": cls.boarding_point.id,
        }

    def test_CT_1_1_email_valido_CV_1(self):
        data = self.valid_data.copy()
        serializer = StudentCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_CT_1_2_email_invalido_CI_1(self):
        data = self.valid_data.copy()
        data["email"] = "existente@email.com"
        serializer = StudentCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertEqual(
            str(serializer.errors["email"][0]), "This email is already in use"
        )

    def test_CT_1_4_senha_invalida_CI_2(self):
        data = self.valid_data.copy()
        data["password"] = "123"
        serializer = StudentCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertIn("at least 8 characters", str(serializer.errors["password"][0]))

    def test_CT_1_5_senha_invalida_CI_3(self):
        data = self.valid_data.copy()
        data["password"] = "SenhaSemNumero"
        serializer = StudentCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertIn("at least one number", str(serializer.errors["password"][0]))

    def test_CT_1_6_senha_invalida_CI_4(self):
        data = self.valid_data.copy()
        data["password"] = "123456789"
        serializer = StudentCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertIn("at least one letter", str(serializer.errors["password"][0]))

    def test_CT_1_8_telefone_invalido_CI_5(self):
        data = self.valid_data.copy()
        data["phone"] = "12345"
        serializer = StudentCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)
        self.assertIn("10 or 11 digits", str(serializer.errors["phone"][0]))

    def test_CT_1_9_telefone_invalido_CI_7(self):
        data = self.valid_data.copy()
        data["phone"] = "8699988a776"
        serializer = StudentCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)
        self.assertIn("10 or 11 digits", str(serializer.errors["phone"][0]))
