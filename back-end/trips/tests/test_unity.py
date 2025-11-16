from django.test import TestCase
from trips.models import Trip, Student
from django.contrib.auth.models import User
from trips.views import TripCreateView, TripCompleteView
from trips.serializers import TripSerializer, TripDetailSerializer
from polls.models import Poll
from datetime import date


class TripsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="José")
        self.student1 = Student.objects.create

    def test_ct01_default_status_is_pending(self):
        poll = Poll.objects.create(date=date(2025, 9, 13), status="open")
        trip = Trip.objects.create(poll=poll, trip_type="outbound")
        self.assertEqual(trip.status, "pending")
