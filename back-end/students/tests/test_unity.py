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


# Tabela 2
class StudentCreateSerializerCreateTests(TestCase):

    def setUp(self):
        self.boarding_point = BoardingPoint.objects.create(
            name="Ponto Teste", route_order=1
        )
        self.valid_data = {
            "name": "Aluno Criado",
            "phone": "86999887766",
            "class_shift": "M",
            "university": "UESPI",
            "email": "aluno.criado@email.com",
            "password": "Password123",
            "boarding_point": self.boarding_point.id,
        }

    @patch("django.contrib.auth.models.User.objects.create_user")
    @patch("django.contrib.auth.models.Group.objects.get_or_create")
    @patch("students.models.Student.objects.create")
    def test_CT_2_1_metodo_create_CV_1(
        self, mock_create_student, mock_get_or_create_group, mock_create_user
    ):

        mock_user = Mock(spec=User)
        mock_create_user.return_value = mock_user

        mock_group = Mock(spec=Group)
        mock_get_or_create_group.return_value = (mock_group, True)

        mock_student = Mock(spec=Student)
        mock_create_student.return_value = mock_student

        serializer = StudentCreateSerializer(data=self.valid_data)

        if not serializer.is_valid():
            print("Erros de Validação no Teste 2.1:", serializer.errors)

        self.assertTrue(serializer.is_valid())

        student = serializer.save()

        mock_create_user.assert_called_once_with(
            username="aluno.criado@email.com",
            email="aluno.criado@email.com",
            password="Password123",
        )

        mock_get_or_create_group.assert_called_once_with(name="students")
        mock_user.groups.add.assert_called_once_with(mock_group)

        expected_student_data = {
            "name": "Aluno Criado",
            "phone": "86999887766",
            "class_shift": "M",
            "university": "UESPI",
            "boarding_point": self.boarding_point,
        }

        mock_create_student.assert_called_once_with(
            user=mock_user, **expected_student_data
        )

        self.assertEqual(student, mock_student)


# Tabela 3
class StudentSerializerGetMethodsTests(TestCase):

    def setUp(self):
        user_a = User.objects.create_user("aluno_a", "a@a.com", "pass123")
        user_b = User.objects.create_user("aluno_b", "b@b.com", "pass123")

        self.student_sem_pagamento = Student.objects.create(
            user=user_a,
            name="Aluno A",
            class_shift="M",
            university="UESPI",
            monthly_payment_cents=None,
            last_payment_date=None,
        )

        self.student_com_pagamento = Student.objects.create(
            user=user_b,
            name="Aluno B",
            class_shift="N",
            university="IFPI",
            monthly_payment_cents=33000,
            last_payment_date=date(2025, 10, 10),
        )

    def test_CT_3_1_pagamento_cents_none_CV_1(self):
        serializer = StudentSerializer(self.student_sem_pagamento)
        self.assertEqual(serializer.data["monthly_payment_cents"], "não informado")

    def test_CT_3_2_pagamento_cents_valor_CV_2(self):
        serializer = StudentSerializer(self.student_com_pagamento)
        self.assertEqual(serializer.data["monthly_payment_cents"], 33000)

    def test_CT_3_3_pagamento_data_none_CV_1(self):
        serializer = StudentSerializer(self.student_sem_pagamento)
        self.assertEqual(serializer.data["last_payment_date"], "não informado")

    def test_CT_3_4_pagamento_data_valor_CV_2(self):
        serializer = StudentSerializer(self.student_com_pagamento)
        self.assertEqual(serializer.data["last_payment_date"], date(2025, 10, 10))


# Tabela 4
class StudentPaymentListViewGetQuerysetTests(TestCase):

    def setUp(self):
        user_a = User.objects.create_user("aluno_a", "a@a.com", "pass123")
        user_b = User.objects.create_user("aluno_b", "b@b.com", "pass123")
        user_c = User.objects.create_user("aluno_c", "c@c.com", "pass123")

        self.aluno_a_pago = Student.objects.create(
            user=user_a,
            name="Aluno A",
            class_shift="M",
            university="UESPI",
            monthly_payment_cents=33000,
            last_payment_date=date.today(),
        )
        self.aluno_b_nao_pago_cents = Student.objects.create(
            user=user_b,
            name="Aluno B",
            class_shift="N",
            university="IFPI",
            monthly_payment_cents=None,
            last_payment_date=date.today(),
        )
        self.aluno_c_nao_pago_data = Student.objects.create(
            user=user_c,
            name="Aluno C",
            class_shift="M",
            university="UESPI",
            monthly_payment_cents=33000,
            last_payment_date=None,
        )

        self.view = StudentPaymentListView()

    def test_CT_4_1_filtro_paid_CV_1(self):
        request = Mock()
        request.query_params = {"payment_status": "paid"}
        self.view.request = request

        queryset = self.view.get_queryset()

        self.assertEqual(list(queryset), [self.aluno_a_pago])

    def test_CT_4_2_filtro_not_paid_CV_2(self):
        request = Mock()
        request.query_params = {"payment_status": "not_paid"}
        self.view.request = request

        queryset = self.view.get_queryset()

        self.assertEqual(queryset.count(), 2)
        self.assertIn(self.aluno_b_nao_pago_cents, queryset)
        self.assertIn(self.aluno_c_nao_pago_data, queryset)

    def test_CT_4_3_sem_filtro_CV_3(self):
        request = Mock()
        request.query_params = {}
        self.view.request = request

        queryset = self.view.get_queryset()

        self.assertEqual(queryset.count(), 3)