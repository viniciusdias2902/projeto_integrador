from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User, Group
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Student


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
