from django.test import TestCase
from trips.models import Trip
from students.models import Student
from polls.models import Poll, Vote
from boarding_points.models import BoardingPoint
from django.contrib.auth.models import User
from trips.views import TripCreateView, TripCompleteView
from trips.serializers import TripSerializer, TripDetailSerializer
from polls.models import Poll
from datetime import date


class TripsTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")
        self.student1 = Student.objects.create(
            name="José", user=self.user1, university="UESPI"
        )
        self.student2 = Student.objects.create(
            name="Leonardo", user=self.user2, university="CHRISFAPI"
        )
        self.boarding_point1 = BoardingPoint.objects.create(
            name="Point 1", route_order=1
        )
        self.boarding_point2 = BoardingPoint.objects.create(
            name="Point2", route_order=2
        )
        self.student1.boarding_point = self.boarding_point1
        self.student1.save()
        self.student2.boarding_point = self.boarding_point2
        self.student2.save()

        self.poll = Poll.objects.create(date=date.today(), status="open")
        Vote.objects.create(student=self.student1, poll=self.poll, option="round_trip")
        Vote.objects.create(
            student=self.student2, poll=self.poll, option="one_way_outbound"
        )

        self.trip_outbound = Trip.objects.create(poll=self.poll, trip_type="outbound")
        self.trip_return = Trip.objects.create(poll=self.poll, trip_type="return")

    def test_ct01_default_status_is_pending(self):
        poll = Poll.objects.create(date=date(2025, 9, 13), status="open")
        trip = Trip.objects.create(poll=poll, trip_type="outbound")
        self.assertEqual(trip.status, "pending")

    def test_ct02_str_method(self):
        self.assertIn("Trip outbound", str(self.trip_outbound))
        self.assertIn(str(self.poll.date), str(self.trip_outbound))

    def test_ct03_start_outbound_trip_sets_first_boarding_point(self):
        first_point = self.trip_outbound.start_trip()
        self.assertEqual(first_point, self.boarding_point1)
        self.assertEqual(self.trip_outbound.status, "in_progress")
        self.assertEqual(
            self.trip_outbound.current_boarding_point, self.boarding_point1
        )
        self.assertIsNotNone(self.trip_outbound.started_at)
