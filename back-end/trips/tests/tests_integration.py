from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import date, timedelta

from students.models import Student
from boarding_points.models import BoardingPoint
from polls.models import Poll, Vote
from .models import Trip
from .serializers import TripSerializer

class TripAPITestCase(APITestCase):

    def setUp(self):
      
        # Usuários
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

        # pontos de Embarque (ordenados)
        self.ponto_a = BoardingPoint.objects.create(
            name="Ponto A (Praça)", route_order=0
        )
        self.ponto_b = BoardingPoint.objects.create(
            name="Ponto B (Posto)", route_order=1
        )

        # Alunos 
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
        
        self.poll_empty = Poll.objects.create(date=date.today() + timedelta(days=1))
        self.trip_outbound_empty = Trip.objects.create(poll=self.poll_empty, trip_type="outbound")
        self.trip_return_empty = Trip.objects.create(poll=self.poll_empty, trip_type="return")


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


    def test_trip_str_method(self):
        expected_str = f"Trip outbound for {self.poll.date} - pending"
        self.assertEqual(str(self.trip_outbound), expected_str)

    def test_admin_can_create_trip(self):
        self.authenticate_admin()
        new_poll = Poll.objects.create(date=date.today() + timedelta(days=2))
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

    def test_admin_can_list_and_filter_trips(self):
        self.authenticate_admin()
        url = reverse("trip-list")
        
        response = self.client.get(url, {"status": "pending"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        
        response = self.client.get(url, {"trip_type": "return"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        response = self.client.get(url, {"poll_id": self.poll_empty.id})
        self.assertEqual(len(response.data), 2)


    def test_start_outbound_trip_successfully(self):
        self.authenticate_admin()
        url = reverse("trip-start", args=[self.trip_outbound.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.trip_outbound.refresh_from_db()
        self.assertEqual(self.trip_outbound.status, "in_progress")
        self.assertEqual(self.trip_outbound.current_boarding_point, self.ponto_a)
        self.assertEqual(response.data["student_count"], 2)

    def test_next_stop_outbound_trip(self):
        self.authenticate_admin()
        self.trip_outbound.start_trip() 
        url = reverse("trip-next-stop", args=[self.trip_outbound.id])
        response = self.client.post(url) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.trip_outbound.refresh_from_db()
        self.assertEqual(self.trip_outbound.current_boarding_point, self.ponto_b)
        self.assertEqual(response.data["student_count"], 1)
        self.assertEqual(response.data["students"][0]["name"], "Carla Dias")

    def test_last_stop_outbound_completes_trip_and_creates_return_trip(self):
        self.authenticate_admin()
        self.trip_outbound.start_trip()
        self.trip_outbound.next_stop() 
        url = reverse("trip-next-stop", args=[self.trip_outbound.id])
        response = self.client.post(url) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.trip_outbound.refresh_from_db()
        self.assertEqual(self.trip_outbound.status, "completed")
        self.assertEqual(response.data["message"], "Outbound trip completed, return trip ready")

    
    def test_start_return_trip_successfully(self):
        self.authenticate_admin()
        url = reverse("trip-start", args=[self.trip_return.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.trip_return.refresh_from_db()
        
        self.assertEqual(self.trip_return.status, "in_progress")
        self.assertEqual(self.trip_return.current_university, "IFPI")
        
        self.assertEqual(response.data["message"], "Return trip started")
        self.assertEqual(response.data["current_university"], "IFPI")
        
      
        self.assertEqual(response.data["student_count"], 1) 
        self.assertEqual(response.data["students"][0]["name"], "Carla Dias")
        
    def test_next_stop_return_trip(self):
        self.authenticate_admin()
        self.trip_return.start_trip() 
        url = reverse("trip-next-stop", args=[self.trip_return.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.trip_return.refresh_from_db()
        self.assertEqual(self.trip_return.current_university, "UESPI")
        self.assertEqual(response.data["student_count"], 1) # Apenas Ana
        self.assertEqual(response.data["students"][0]["name"], "Ana Silva")

    def test_last_stop_return_completes_trip(self):
        self.authenticate_admin()
        self.trip_return.start_trip()
        self.trip_return.next_stop() 
        url = reverse("trip-next-stop", args=[self.trip_return.id])
        response = self.client.post(url) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.trip_return.refresh_from_db()
        self.assertEqual(self.trip_return.status, "completed")
        self.assertEqual(response.data["message"], "Return trip completed")

        
    def test_start_trip_outbound_no_points(self):
        self.authenticate_admin()
        url = reverse("trip-start", args=[self.trip_outbound_empty.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No boarding points", response.data["error"])

    def test_start_trip_return_no_universities(self):
        self.authenticate_admin()
        url = reverse("trip-start", args=[self.trip_return_empty.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No universities", response.data["error"])

    def test_cannot_start_started_trip(self):
        self.authenticate_admin()
        self.trip_outbound.start_trip() # Inicia
        url = reverse("trip-start", args=[self.trip_outbound.id])
        response = self.client.post(url) # Tenta iniciar de novo
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already started", response.data["error"])

    def test_cannot_advance_pending_trip(self):
        self.authenticate_admin()
        url = reverse("trip-next-stop", args=[self.trip_outbound.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("not in progress", response.data["error"])

    def test_cannot_advance_completed_trip(self):
        self.authenticate_admin()
        self.trip_outbound.start_trip()
        self.trip_outbound.next_stop()
        self.trip_outbound.next_stop()
        self.assertEqual(self.trip_outbound.status, "completed")
        
        url = reverse("trip-next-stop", args=[self.trip_outbound.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("not in progress", response.data["error"])

    def test_admin_can_complete_trip_manually(self):
        self.authenticate_admin()
        self.trip_outbound.start_trip() 
        url = reverse("trip-complete", args=[self.trip_outbound.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.trip_outbound.refresh_from_db()
        self.assertEqual(self.trip_outbound.status, "completed")
        self.assertIn("Outbound trip completed manually", response.data["message"])

    def test_admin_can_complete_return_trip_manually(self):
        self.authenticate_admin()
        self.trip_return.start_trip() 
        url = reverse("trip-complete", args=[self.trip_return.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.trip_return.refresh_from_db()
        self.assertEqual(self.trip_return.status, "completed")
        self.assertIn("Return trip completed", response.data["message"])

    def test_cannot_complete_pending_trip(self):
        self.authenticate_admin()
        url = reverse("trip-complete", args=[self.trip_outbound.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("not in progress", response.data["error"])

    def test_model_getters_return_empty_for_wrong_trip_type(self):
        self.assertEqual(self.trip_return.get_boarding_points(), [])
        self.assertEqual(self.trip_outbound.get_universities(), [])
        self.assertEqual(self.trip_return.get_students_at_point(self.ponto_a), [])
        self.assertEqual(self.trip_outbound.get_students_at_university("IFPI"), [])

    def test_student_can_get_trip_status_on_outbound_trip(self):
        self.authenticate_student()
        self.trip_outbound.start_trip() 
        url = reverse("trip-status", args=[self.trip_outbound.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["trip"]["status"], "in_progress")
        self.assertEqual(response.data["trip"]["current_boarding_point"]["name"], "Ponto A (Praça)")
        self.assertEqual(response.data["current_student_count"], 2)
        student_names = sorted([s["name"] for s in response.data["current_students"]])
        self.assertEqual(student_names, ["Ana Silva", "Bruno Costa"])

    def test_student_can_get_trip_status_on_return_trip(self):
        self.authenticate_student(self.student_user_3) 
        self.trip_return.start_trip()
        
        url = reverse("trip-status", args=[self.trip_return.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["trip"]["status"], "in_progress")
        self.assertIsNone(response.data["trip"]["current_boarding_point"]) 
        self.assertEqual(response.data["trip"]["current_university"], "IFPI")
        self.assertEqual(response.data["current_student_count"], 1)
        self.assertEqual(response.data["current_students"][0]["name"], "Carla Dias")
        
    def test_trip_detail_serializer_for_outbound_trip(self):
        self.authenticate_admin()
        self.trip_outbound.start_trip()
        url = reverse("trip-detail", args=[self.trip_outbound.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("stops", response.data)
        stops = response.data["stops"]
        self.assertEqual(len(stops), 2)
        self.assertEqual(stops[0]["boarding_point"]["name"], "Ponto A (Praça)")
        self.assertEqual(stops[0]["student_count"], 2)
        self.assertEqual(stops[0]["is_current"], True)
        self.assertEqual(stops[1]["boarding_point"]["name"], "Ponto B (Posto)")
        self.assertEqual(stops[1]["student_count"], 1)
        self.assertEqual(stops[1]["is_current"], False)

    def test_trip_detail_serializer_for_return_trip(self):
        self.authenticate_admin()
        self.trip_return.start_trip() 
        url = reverse("trip-detail", args=[self.trip_return.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("stops", response.data)
        stops = response.data["stops"]
        self.assertEqual(len(stops), 2)
        self.assertEqual(stops[0]["university"], "IFPI")
        self.assertEqual(stops[0]["student_count"], 1)
        self.assertEqual(stops[0]["is_current"], True)
        self.assertEqual(stops[1]["university"], "UESPI")
        self.assertEqual(stops[1]["student_count"], 1)
        self.assertEqual(stops[1]["is_current"], False)

    def test_trip_serializer_indexes_on_pending_return_trip(self):
        self.authenticate_admin()
        url = reverse("trip-detail", args=[self.trip_return.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_stops"], 2) 
        self.assertIsNone(response.data["current_stop_index"]) 
        self.assertIsNone(response.data["current_university_name"]) 
    
    def test_model_getters_on_pending_trip(self):
        self.assertEqual(self.trip_outbound.status, "pending")
        students = self.trip_outbound.get_current_students()
        self.assertEqual(students, [])

    def test_serializer_fields_on_pending_trip(self):  
        trip = self.trip_return
        self.assertEqual(trip.status, "pending")
        
        serializer = TripSerializer(trip)
        data = serializer.data
        
        self.assertIsNone(data["current_stop_index"]) 
        self.assertIsNone(data["current_university_name"])

    def test_model_edge_case_next_stop_with_no_current_point(self):
        self.trip_outbound.status = "in_progress"
        self.trip_outbound.current_boarding_point = None
        self.trip_outbound.save()
        
        with self.assertRaisesMessage(ValueError, "No current boarding point"):
            self.trip_outbound.next_stop()

    def test_model_edge_case_next_stop_with_mismatched_point(self):
        fake_point = BoardingPoint.objects.create(name="Ponto Falso", route_order=99)
        
        self.trip_outbound.status = "in_progress"
        self.trip_outbound.current_boarding_point = fake_point
        self.trip_outbound.save()
        
        with self.assertRaisesMessage(ValueError, "Current boarding point not found"):
            self.trip_outbound.next_stop()

    def test_serializer_edge_case_stop_index_with_no_current_point(self):
        self.trip_outbound.status = "in_progress"
        self.trip_outbound.current_boarding_point = None
        self.trip_outbound.save()
        
        serializer = TripSerializer(self.trip_outbound)
        
        #serializer deve tratar esse errp graciosamente e retornar um None
        self.assertIsNone(serializer.data["current_stop_index"])