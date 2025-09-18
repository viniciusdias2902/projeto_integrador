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

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def authenticate_as_student(self, student_user):
        token = self.get_jwt_token(student_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def authenticate_as_admin(self):
        token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_student_can_create_vote(self):
        self.authenticate_as_student(self.student_user_1)

        url = reverse("vote-create")
        payload = {"poll": self.poll.id, "option": "round_trip"}

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        vote = Vote.objects.get(id=response.data["id"])
        self.assertEqual(vote.student, self.student_1)
        self.assertEqual(vote.poll, self.poll)

    def test_student_cannot_vote_twice_on_same_poll(self):
        self.authenticate_as_student(self.student_user_1)
        url = reverse("vote-create")
        payload = {"poll": self.poll.id, "option": "round_trip"}

        response1 = self.client.post(url, payload, format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        payload["option"] = "absent"
        response2 = self.client.post(url, payload, format="json")

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            Vote.objects.filter(student=self.student_1, poll=self.poll).count(), 1
        )

    def test_student_can_list_only_own_votes(self):
        Vote.objects.create(
            student=self.student_1, poll=self.poll, option="one_way_outbound"
        )
        Vote.objects.create(student=self.student_2, poll=self.poll, option="absent")
        self.authenticate_as_student(self.student_user_1)
        url = reverse("vote-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]["student"]["name"], self.student_1.name)

    def test_authenticated_user_can_get_boarding_list(self):
        Vote.objects.create(student=self.student_1, poll=self.poll, option="round_trip")
        Vote.objects.create(
            student=self.student_2, poll=self.poll, option="one_way_outbound"
        )

        self.authenticate_as_admin()

        url = reverse("poll-boarding-list", args=[self.poll.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        boarding_list_string = response.data["boarding_list"]
        self.assertIn(self.student_1.name, boarding_list_string)
        self.assertIn(self.student_2.name, boarding_list_string)
        self.assertEqual(boarding_list_string.count(","), 1)