from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User, Group
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Student
from boarding_points.models import BoardingPoint
from datetime import date, timedelta


class StudentAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.group, _ = Group.objects.get_or_create(name="students")
        self.user.groups.add(self.group)

        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass"
        )

        self.student_data = {
            "name": "Isaac Newton",
            "phone": "1234567890",
            "class_shift": "M",
            "university": "UESPI",
            "email": "isaac.newton@example.com",
            "password": "Password123",
        }

        self.student = Student.objects.create(
            user=self.user,
            name="Existing Student",
            phone="0987654321",
            class_shift="E",
            university="IFPI",
        )

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def authenticate_admin(self):
        token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_create_student(self):
        url = reverse("students-create-list")
        response = self.client.post(url, self.student_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Student.objects.filter(name="Isaac Newton").exists())

    def test_list_students_authenticated(self):
        self.authenticate_admin()
        url = reverse("students-create-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_student(self):
        self.authenticate_admin()
        url = reverse("students-retrieve-update-destroy", args=[self.student.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Existing Student")

    def test_update_student(self):
        self.authenticate_admin()
        url = reverse("students-retrieve-update-destroy", args=[self.student.id])
        data = {
            "name": "Updated Name",
            "phone": "1112223334",
            "class_shift": "M",
            "university": "CHRISFAPI",
            "role": self.student.role,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, "Updated Name")

    def test_delete_student(self):
        self.authenticate_admin()
        url = reverse("students-retrieve-update-destroy", args=[self.student.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Student.objects.filter(id=self.student.id).exists())


class StudentPaymentAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass"
        )

        self.regular_user = User.objects.create_user(
            username="regularuser", password="regularpass"
        )

        self.student1 = Student.objects.create(
            user=User.objects.create_user(
                username="student1@test.com", password="pass123"
            ),
            name="Student One",
            phone="1111111111",
            class_shift="M",
            university="UESPI",
        )

        self.student2 = Student.objects.create(
            user=User.objects.create_user(
                username="student2@test.com", password="pass123"
            ),
            name="Student Two",
            phone="2222222222",
            class_shift="A",
            university="IFPI",
            monthly_payment_cents=50000,
            last_payment_date=date.today() - timedelta(days=15),
        )

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def authenticate_admin(self):
        token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def authenticate_regular_user(self):
        token = self.get_jwt_token(self.regular_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_student_payment_fields_return_not_informed_when_null(self):
        self.authenticate_admin()
        url = reverse("students-retrieve-update-destroy", args=[self.student1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["monthly_payment_cents"], "não informado")
        self.assertEqual(response.data["last_payment_date"], "não informado")

    def test_student_payment_fields_return_values_when_set(self):
        self.authenticate_admin()
        url = reverse("students-retrieve-update-destroy", args=[self.student2.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["monthly_payment_cents"], 50000)
        self.assertIsNotNone(response.data["last_payment_date"])

    def test_admin_can_update_student_payment(self):
        self.authenticate_admin()
        url = reverse("student-payment-update", args=[self.student1.id])
        payment_date = (date.today() - timedelta(days=10)).isoformat()
        data = {"monthly_payment_cents": 45000, "last_payment_date": payment_date}

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student1.refresh_from_db()
        self.assertEqual(self.student1.monthly_payment_cents, 45000)
        self.assertEqual(self.student1.last_payment_date.isoformat(), payment_date)

    def test_regular_user_cannot_update_payment(self):
        self.authenticate_regular_user()
        url = reverse("student-payment-update", args=[self.student1.id])
        data = {
            "monthly_payment_cents": 45000,
            "last_payment_date": date.today().isoformat(),
        }

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_all_payments(self):
        self.authenticate_admin()
        url = reverse("student-payment-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_admin_can_filter_paid_students(self):
        self.authenticate_admin()
        url = reverse("student-payment-list")

        response = self.client.get(url, {"payment_status": "paid"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Student Two")

    def test_admin_can_filter_unpaid_students(self):
        self.authenticate_admin()
        url = reverse("student-payment-list")

        response = self.client.get(url, {"payment_status": "not_paid"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Student One")

    def test_admin_can_bulk_update_payments(self):
        self.authenticate_admin()
        url = reverse("student-payment-bulk-update")

        payment_date = date.today().isoformat()
        data = {
            "student_ids": [self.student1.id, self.student2.id],
            "monthly_payment_cents": 60000,
            "last_payment_date": payment_date,
        }

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["updated_count"], 2)

        self.student1.refresh_from_db()
        self.student2.refresh_from_db()

        self.assertEqual(self.student1.monthly_payment_cents, 60000)
        self.assertEqual(self.student1.last_payment_date.isoformat(), payment_date)
        self.assertEqual(self.student2.monthly_payment_cents, 60000)
        self.assertEqual(self.student2.last_payment_date.isoformat(), payment_date)

    def test_monthly_payment_validation(self):
        self.authenticate_admin()
        url = reverse("student-payment-update", args=[self.student1.id])

        data = {"monthly_payment_cents": -1000}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
