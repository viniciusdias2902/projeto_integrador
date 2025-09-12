from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from students.models import Student
from .models import Poll, Vote
from datetime import date


class PollsAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass"
        )

        self.student_user_1 = User.objects.create_user(
            username="aluno_ana", password="testpass123"
        )
        self.student_1 = Student.objects.create(
            user=self.student_user_1,
            name="Ana Silva",
            phone="111111111",
            class_shift="M",
            university="UESPI",
        )

        self.student_user_2 = User.objects.create_user(
            username="aluno_bruno", password="testpass123"
        )
        self.student_2 = Student.objects.create(
            user=self.student_user_2,
            name="Bruno Costa",
            phone="222222222",
            class_shift="E",
            university="IFPI",
        )

        self.poll = Poll.objects.create(date=date.today())