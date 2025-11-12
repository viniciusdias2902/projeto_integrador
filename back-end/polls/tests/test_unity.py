from django.test import TestCase
from polls.models import Poll
from django.contrib.auth.models import User
from polls.views import PollListView, PollDetailView, PollBoardingListView
from polls.serializers import PollSerializer
from datetime import date


class PollsTest(TestCase):
    def test_ct01_str_method(self):
        poll = Poll.objects.create(date=date(2025, 8, 14), status="open")
        self.assertEqual(str(poll), "Poll for 2025-08-14 (open)")
