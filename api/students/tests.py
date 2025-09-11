from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Student


class StudentCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = Student.objects.create(
            name="Michael Corleone",
            phone="1234567890",
            class_shift="Night",
            university="UESPI",
            email="michaelcorleone@gmail.com",
            password="antony1945",
        )
        self.valid_student_data = {
            "name": "Joe Potter",
            "phone": "0987654321",
            "class_shift": "Morning",
            "university": "IFPI",
            "email": "joepotter15@gmail.com",
            "password": "kdieuaj56",
        }

    def test_create_student(self):
        url = reverse("students-create-list")
        response = self.client.post(url, self.valid_student_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.get(id=response.data["id"]).name, "Joe Potter")

    def test_list_students(self):
        url = reverse("students-create-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_student(self):
        url = reverse("student-retrieve-update-destroy", args=[self.student.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Michael Corleone")

    def test_update_student(self):
        url = reverse("student-retrieve-update-destroy", args=[self.student.id])
        updated_data = {
            "name": "Nina",
            "phone": "1231231234",
            "class_shift": "Afternoon",
            "university": "CHRISFAPI",
            "email": "ninasayers@gmail.com",
            "password": "blackswan",
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Nina")

    def test_delete_student(self):
        url = reverse("student-retrieve-update-destroy", args=[self.student.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)
