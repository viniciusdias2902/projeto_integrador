from django.test import TestCase
from polls.models import Poll, Vote, Student
from django.contrib.auth.models import User
from polls.views import PollListView, PollDetailView, PollBoardingListView
from polls.serializers import PollSerializer
from datetime import date, timedelta, datetime, time
from django.utils import timezone
from django.db import IntegrityError
from unittest.mock import patch


class PollsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="teste_user")
        self.student = Student.objects.create(name="Teste enquetes", user=self.user)
        self.poll_today = Poll.objects.create(date=timezone.localdate())
        self.poll_yesterday = Poll.objects.create(
            date=timezone.localdate() - timedelta(days=1), status="open"
        )
        self.poll_tomorrow = Poll.objects.create(
            date=timezone.localdate() + timedelta(days=1), status="open"
        )

    def test_ct01_str_method(self):
        poll = Poll.objects.create(date=date(2025, 8, 14), status="open")
        self.assertEqual(str(poll), "Poll for 2025-08-14 (open)")

    def test_ct02_create_valid_vote(self):
        vote = Vote.objects.create(
            student=self.student, poll=self.poll_today, option="round_trip"
        )
        self.assertIsNotNone(vote.pk)
        self.assertEqual(vote.option, "round_trip")

    def test_ct03_unique_vote_per_poll(self):
        Vote.objects.create(
            student=self.student, poll=self.poll_today, option="round_trip"
        )

        with self.assertRaises(IntegrityError):
            Vote.objects.create(
                student=self.student, poll=self.poll_today, option="absent"
            )

    def test_ct04_can_vote_past_poll(self):
        fake = datetime.combine(timezone.localdate(), time(10, 0))
        with patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = timezone.make_aware(fake)

            self.assertFalse(
                self.poll_yesterday.can_vote_for_option("one_way_outbound")
            )
