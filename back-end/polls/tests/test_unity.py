from django.test import TestCase
from polls.models import Poll, Vote
from django.contrib.auth.models import User
from polls.views import PollListView, PollDetailView, PollBoardingListView
from polls.serializers import PollSerializer
from datetime import date
from students.models import Student
from django.utils import timezone
import pytest


@pytest.fixture
def student(db):
    return Student.objects.create(name="Teste enquetes")


@pytest.fixture
def poll_today(db):
    return Poll.objects.create(date=timezone.localdate())


@pytest.fixture
def poll_tomorrow(db):
    return Poll.objects.create(date=timezone.localdate() + timezone.timedelta(days=1))


@pytest.fixture
def poll_yesterday(db):
    return Poll.objects.create(date=timezone.localdate() - timezone.timedelta(days=1))


class PollsTest(TestCase):
    def test_ct01_str_method(self):
        poll = Poll.objects.create(date=date(2025, 8, 14), status="open")
        self.assertEqual(str(poll), "Poll for 2025-08-14 (open)")
