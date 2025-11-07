from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from students.models import Student
from boarding_points.models import BoardingPoint
from .models import Poll, Vote
from datetime import date, timedelta
from django.utils import timezone
from unittest import mock

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
            boarding_point=self.ponto_a,
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
        print(
            "DEBUG test_student_can_create_vote:", response.status_code, response.data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vote = Vote.objects.get(id=response.data["id"])
        self.assertEqual(vote.student, self.student_1)
        self.assertEqual(vote.poll, self.poll)
        self.assertEqual(vote.option, "round_trip")

    def test_student_cannot_vote_twice_on_same_poll(self):
        Vote.objects.create(student=self.student_1, poll=self.poll, option="round_trip")
        
        self.authenticate_as_student(self.student_user_1)
        url = reverse("vote-create")
        payload = {"poll": self.poll.id, "option": "absent"}
        response2 = self.client.post(url, payload, format="json")
        
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Você já votou", str(response2.data))
        self.assertEqual(
            Vote.objects.filter(student=self.student_1, poll=self.poll).count(), 1
        )

    def test_student_can_list_only_own_votes(self):
        Vote.objects.create(student=self.student_1, poll=self.poll, option="one_way_outbound")
        Vote.objects.create(student=self.student_2, poll=self.poll, option="absent")
        
        self.authenticate_as_student(self.student_user_1)
        url = reverse("vote-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["student"]["name"], self.student_1.name)

    def test_get_boarding_list_grouped_by_point(self):
        Vote.objects.create(student=self.student_1, poll=self.poll, option="round_trip")
        Vote.objects.create(student=self.student_2, poll=self.poll, option="one_way_outbound")
        
        self.authenticate_as_admin()
        url = reverse("poll-boarding-list", args=[self.poll.id])
        url += "?trip_type=outbound" 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)

        ponto_a_data = response.data[0]
        self.assertEqual(ponto_a_data["point"]["name"], "Ponto A - Praça Central")
        self.assertEqual(len(ponto_a_data["students"]), 2) 

        nomes_ponto_a = sorted([s["name"] for s in ponto_a_data["students"]])
        self.assertEqual(nomes_ponto_a, ["Ana Silva", "Bruno Costa"])

    def test_get_boarding_list_requires_trip_type_param(self):
        self.authenticate_as_admin()
        url = reverse("poll-boarding-list", args=[self.poll.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_boarding_list_empty_if_no_votes(self):
        self.authenticate_as_admin()
        url = reverse("poll-boarding-list", args=[self.poll.id])
        url += "?trip_type=return" 
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_boarding_list_grouped_by_university_for_return(self):
       
        Vote.objects.create(student=self.student_1, poll=self.poll, option="round_trip")
        Vote.objects.create(student=self.student_2, poll=self.poll, option="one_way_return") 

        self.authenticate_as_admin()
        url = reverse("poll-boarding-list", args=[self.poll.id])
        url += "?trip_type=return" 
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), 2)
        
        group_ifpi = response.data[0]
        self.assertEqual(group_ifpi["group_name"], "IFPI")
        self.assertEqual(len(group_ifpi["students"]), 1)
        self.assertEqual(group_ifpi["students"][0]["name"], "Bruno Costa")
        
        group_uespi = response.data[1]
        self.assertEqual(group_uespi["group_name"], "UESPI")
        self.assertEqual(len(group_uespi["students"]), 1)
        self.assertEqual(group_uespi["students"][0]["name"], "Ana Silva")

    def test_student_cannot_vote_outbound_after_deadline(self):
        self.authenticate_as_student(self.student_user_1)
        url = reverse("vote-create")
        
        poll_date = date.today()
        mock_time = timezone.make_aware(
            timezone.datetime.combine(poll_date, timezone.datetime.min.time()) + 
            timezone.timedelta(hours=13)
        )
        
        with mock.patch('django.utils.timezone.now', return_value=mock_time):
            payload = {"poll": self.poll.id, "option": "one_way_outbound"}
            response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("até 12:00", str(response.data))

    def test_student_cannot_vote_return_after_deadline(self):
        self.authenticate_as_student(self.student_user_1)
        url = reverse("vote-create")
        
        poll_date = date.today()
        mock_time = timezone.make_aware(
            timezone.datetime.combine(poll_date, timezone.datetime.min.time()) + 
            timezone.timedelta(hours=20)
        )
        
        with mock.patch('django.utils.timezone.now', return_value=mock_time):
            payload = {"poll": self.poll.id, "option": "one_way_return"}
            response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("até 18:00", str(response.data))

    def test_admin_can_trigger_create_weekly_polls(self):
        self.authenticate_as_admin()
        Poll.objects.filter(date__gte=date.today()).delete()
        
        url = reverse("create-weekly-polls")
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Processo de criação de enquetes concluído", response.data["message"])
        self.assertGreater(response.data["total_created"], 0)
        self.assertTrue(Poll.objects.filter(date__gte=date.today()).exists())

    def test_admin_can_trigger_clean_old_polls(self):
        self.authenticate_as_admin()
        
        old_poll = Poll.objects.create(date=date.today() - timedelta(days=5))
        self.assertTrue(Poll.objects.filter(id=old_poll.id).exists())
        
        url = reverse("clean-old-polls")
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["deleted_count"], 1)
        self.assertFalse(Poll.objects.filter(id=old_poll.id).exists())