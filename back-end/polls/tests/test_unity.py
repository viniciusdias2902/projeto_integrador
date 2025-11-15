from django.test import TestCase
from polls.models import Poll, Vote
from django.contrib.auth.models import User
from polls.views import PollListView, PollDetailView, PollBoardingListView
from polls.serializers import PollSerializer
from datetime import date

class PollsTest(TestCase):
    def setUp(self):
    def test_ct01_str_method(self):
        poll = Poll.objects.create(date=date(2025, 8, 14), status="open")
        self.assertEqual(str(poll), "Poll for 2025-08-14 (open)")

    def test_ct02_create_valid_vote(self)::
        vote = Vote.objects.create(
            student=student, poll=poll_today, option="round_trip"
        )
        assert vote.pk is not None
        assert vote.option == "round_trip"
