from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from students.models import Student
from common.models import BoardingPoint
from .models import Poll, Vote
from datetime import date


class PollsAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass"
        )
        
        self.ponto_a = BoardingPoint.objects.create(
            name="Ponto A - Praça Central", route_order=0
        )
        self.ponto_b = BoardingPoint.objects.create(
            name="Ponto B - Posto Shell", route_order=1
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
            boarding_point=self.ponto_a,
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
            boarding_point=self.ponto_b,
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

   
    def test_get_boarding_list_grouped_by_point(self):
        Vote.objects.create(student=self.student_1, poll=self.poll, option="round_trip")
        Vote.objects.create(
            student=self.student_2, poll=self.poll, option="one_way_outbound"
        )

        self.authenticate_as_admin()

        url = reverse("poll-boarding-list", args=[self.poll.id])
        url += "?trip_type=one_way_outbound" 

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)

        ponto_a_data = response.data[0]
        self.assertEqual(ponto_a_data["point"]["name"], "Ponto A - Praça Central")
        self.assertEqual(len(ponto_a_data["students"]), 1) 

        nomes_ponto_a = sorted([s["name"] for s in ponto_a_data["students"]])
        self.assertEqual(nomes_ponto_a, ["Ana Silva"])

        ponto_b_data = response.data[1]
        self.assertEqual(ponto_b_data["point"]["name"], "Ponto B - Posto Shell")
        self.assertEqual(len(ponto_b_data["students"]), 1) 
        self.assertEqual(ponto_b_data["students"][0]["name"], "Bruno Costa")