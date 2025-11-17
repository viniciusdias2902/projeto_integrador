from django.test import TestCase
from trips.models import Trip, Student, BoardingPoint, Poll, Vote
from django.contrib.auth.models import User
from trips.views import TripCreateView, TripCompleteView
from trips.serializers import TripSerializer, TripDetailSerializer
from polls.models import Poll
from datetime import date


class TripsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user1")
        self.student1 = Student.objects.create(
            name="José", user=self.user, university="UESPI"
        )
        self.student2 = Student.objects.create(
            name="Leonardo", user=self.user, university="CHRISFAPI"
        )
        self.boarding1 = BoardingPoint.objects.create(name="Point 1", route_order=1)
        self.boarding2 = BoardingPoint.objects.create(name="Point2", route_order=2)
        self.student1.boarding_point = self.boarding1
        self.student1.save()
        self.student2.boarding_point = self.boarding2
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
