from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import date

from students.models import Student
from boarding_points.models import BoardingPoint
from polls.models import Poll, Vote
from .models import Trip

class TripAPITestCase(APITestCase):

    def setUp(self):
       
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass123"
        )
        self.student_user_1 = User.objects.create_user(
            username="ana.silva", password="testpass123"
        )
        self.student_user_2 = User.objects.create_user(
            username="bruno.costa", password="testpass123"
        )
        self.student_user_3 = User.objects.create_user(
            username="carla.dias", password="testpass123"
        )

        self.ponto_a = BoardingPoint.objects.create(
            name="Ponto A (Praça)", route_order=0
        )
        self.ponto_b = BoardingPoint.objects.create(
            name="Ponto B (Posto)", route_order=1
        )

        self.student_ana = Student.objects.create(
            user=self.student_user_1, name="Ana Silva", phone="111",
            class_shift="M", university="UESPI", boarding_point=self.ponto_a
        )
        self.student_bruno = Student.objects.create(
            user=self.student_user_2, name="Bruno Costa", phone="222",
            class_shift="A", university="IFPI", boarding_point=self.ponto_a
        )
        self.student_carla = Student.objects.create(
            user=self.student_user_3, name="Carla Dias", phone="333",
            class_shift="N", university="IFPI", boarding_point=self.ponto_b
        )
        
        self.poll = Poll.objects.create(date=date.today())

        Vote.objects.create(student=self.student_ana, poll=self.poll, option="round_trip")
        Vote.objects.create(student=self.student_bruno, poll=self.poll, option="one_way_outbound")
        Vote.objects.create(student=self.student_carla, poll=self.poll, option="round_trip")

        self.trip_outbound = Trip.objects.create(poll=self.poll, trip_type="outbound")
        self.trip_return = Trip.objects.create(poll=self.poll, trip_type="return")

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def authenticate_admin(self):
        token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        
    def authenticate_student(self, user=None):
        user = user or self.student_user_1
        token = self.get_jwt_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_admin_can_create_trip(self):
        self.authenticate_admin()
        new_poll = Poll.objects.create(date=date.today() + timezone.timedelta(days=1))
        url = reverse("trip-create")
        payload = {"poll": new_poll.id, "trip_type": "outbound"}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Trip.objects.filter(poll=new_poll, trip_type="outbound").exists())

    def test_cannot_create_duplicate_trip(self):
        self.authenticate_admin()
        url = reverse("trip-create")
        payload = {"poll": self.poll.id, "trip_type": "outbound"}
        response = self.client.post(url, payload, format="json")
        
      
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("must make a unique set", str(response.data))