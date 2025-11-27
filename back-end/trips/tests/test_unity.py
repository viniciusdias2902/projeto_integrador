from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from datetime import date
from rest_framework.exceptions import ValidationError
from rest_framework import status
from trips.models import Trip
from trips.serializers import TripSerializer, TripDetailSerializer
from students.models import Student
from polls.models import Poll, Vote
from boarding_points.models import BoardingPoint
from rest_framework.test import APITestCase, APIClient


class TripModelLogicTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")

        # pontos
        self.bp1 = BoardingPoint.objects.create(name="Ponto 1", route_order=0)
        self.bp2 = BoardingPoint.objects.create(name="Ponto 2", route_order=1)

        # alunos
        self.student1 = Student.objects.create(
            name="Aluno Ida",
            user=self.user,
            university="UESPI",
            boarding_point=self.bp1,
        )
        self.user2 = User.objects.create(username="test_user2")
        self.student2 = Student.objects.create(
            name="Aluno Volta",
            user=self.user2,
            university="IFPI",
            boarding_point=self.bp2,
        )

        # enquete e votos
        self.poll = Poll.objects.create(date=date.today())
        Vote.objects.create(
            student=self.student1, poll=self.poll, option="round_trip"
        )  # Vai na Ida
        Vote.objects.create(
            student=self.student2, poll=self.poll, option="one_way_return"
        )  # Só Volta

        # bviagem
        self.trip = Trip.objects.create(poll=self.poll, trip_type="outbound")

    # Fuccionalide 1
    def test_CT_01_initial_status_pending(self):
        self.assertEqual(self.trip.status, "pending")

    # Funcionalidade 1
    def test_CT_02_start_trip_outbound_logic(self):
        first_point = self.trip.start_trip()

        self.assertEqual(self.trip.status, "in_progress")
        self.assertEqual(self.trip.current_boarding_point, self.bp1)
        self.assertIsNotNone(self.trip.started_at)
        self.assertEqual(first_point, self.bp1)

    # Funcionalidade 1
    def test_CT_03_cannot_start_non_pending_trip(self):
        self.trip.status = "in_progress"
        self.trip.save()

        with self.assertRaisesMessage(ValueError, "Trip already started"):
            self.trip.start_trip()

    # Funcionalidade 1
    def test_CT_04_next_stop_advances_point(self):
        Vote.objects.filter(student=self.student2).update(option="round_trip")

        self.trip.start_trip()

        next_point = self.trip.next_stop()

        self.assertEqual(self.trip.current_boarding_point, self.bp2)
        self.assertEqual(next_point, self.bp2)

    # Funcionalidade 1
    def test_CT_05_next_stop_completes_trip_at_end(self):
        self.trip.start_trip()

        self.trip.next_stop()

        self.assertEqual(self.trip.status, "completed")
        self.assertIsNone(self.trip.current_boarding_point)

    # Funcionalidade 1
    def test_CT_06_complete_trip_logic(self):
        self.trip.status = "in_progress"
        self.trip.save()

        self.trip.complete_trip()

        self.assertEqual(self.trip.status, "completed")
        self.assertIsNotNone(self.trip.completed_at)

    # Funcionalidade 2
    def test_CT_07_get_boarding_points_filters_correctly(self):
        points = self.trip.get_boarding_points()

        self.assertEqual(len(points), 1)
        self.assertEqual(points[0], self.bp1)

    # Funcionalidade 2
    def test_CT_08_get_students_at_point(self):
        students = self.trip.get_students_at_point(self.bp1)

        self.assertEqual(len(students), 1)
        self.assertEqual(students[0], self.student1)


class TripSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.poll = Poll.objects.create(date=date.today())
        self.bp1 = BoardingPoint.objects.create(name="Ponto 1", route_order=0)
        self.bp2 = BoardingPoint.objects.create(name="Ponto 2", route_order=1)

        self.student = Student.objects.create(
            name="Tony",
            user=self.user,
            university="UESPI",
            boarding_point=self.bp1,
        )

        Vote.objects.create(student=self.student, poll=self.poll, option="round_trip")
        self.trip = Trip.objects.create(poll=self.poll, trip_type="return")

    # Funcionalidade 3
    def test_CT_09_university_name_mapping(self):
        self.trip.current_university = "UESPI"
        serializer = TripSerializer(self.trip)

        self.assertEqual(
            serializer.data["current_university_name"], "Universidade Estadual do Piaui"
        )

    # Funcionalidade 3
    def test_CT_10_current_stop_index_calculation(self):
        user = User.objects.create(username="u")
        bp1 = BoardingPoint.objects.create(name="P1", route_order=0)
        bp2 = BoardingPoint.objects.create(name="P2", route_order=1)
        student = Student.objects.create(
            name="S", user=user, boarding_point=bp2
        )  # Aluno no ponto 2
        Vote.objects.create(student=student, poll=self.poll, option="round_trip")

        trip_outbound = Trip.objects.create(
            poll=self.poll, trip_type="outbound", status="in_progress"
        )

        trip_outbound.current_boarding_point = bp2
        trip_outbound.save()

        serializer = TripSerializer(trip_outbound)
        self.assertEqual(serializer.data["current_stop_index"], 0)

    def test_CT_11_serializer_accepts_valid_data(self):
        serializer = TripSerializer(instance=self.trip)
        data = serializer.data

        self.assertEqual(data["poll"], self.poll.id)
        self.assertEqual(data["trip_type"], "return")
        self.assertEqual(data["status"], "pending")

    def test_CT_12_current_university_name_none(self):
        self.trip.current_university = None
        serializer = TripSerializer(self.trip)
        self.assertIsNone(serializer.data["current_university_name"])

    def test_CT_13_total_stops_outbound(self):
        serializer = TripSerializer(self.trip)
        self.assertEqual(serializer.data["total_stops"], 1)


class TestsTripView(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user", password="testpass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.poll = Poll.objects.create(date=timezone.now().date(), status="open")

        self.bp1 = BoardingPoint.objects.create(name="Ponto 1", route_order=1)
        self.bp2 = BoardingPoint.objects.create(name="Ponto 2", route_order=2)

        self.student1 = Student.objects.create(
            user=User.objects.create(username="student1"),
            name="Vito",
            phone="999999999",
            university="UESPI",
            boarding_point=self.bp1,
        )

        self.student2 = Student.objects.create(
            user=User.objects.create(username="student2"),
            name="Connie",
            phone="9999994579",
            university="IFPI",
            boarding_point=self.bp2,
        )

        Vote.objects.create(student=self.student1, poll=self.poll, option="round_trip")
        Vote.objects.create(student=self.student2, poll=self.poll, option="outbound")

        self.outbound_trip = Trip.objects.create(poll=self.poll, trip_type="outbound")
        self.return_trip = Trip.objects.create(poll=self.poll, trip_type="return")

    # Funcionalidade 4
    def test_CT_14_list_all_trips(self):
        url = reverse("trip-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_CT_15_list_filter_by_poll(self):
        url = reverse("trip-list") + f"?poll={self.poll.id}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class TestTripDetailView(TestsTripView):
    def test_CT_16_create_trip_sucess(self):
        url = reverse("trip-create")
        data = {"poll": self.poll.id, "trip_type": "return", "status": "pending"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
