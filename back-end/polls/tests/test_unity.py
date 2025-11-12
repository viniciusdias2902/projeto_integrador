from django.test import TestCase
from polls.models import Polls
from django.contrib.auth.models import User
from polls.views import PollListView, PollDetailView, PollBoardingListView
from polls.serializers import PollSerializer


class PollsTest(TestCase):
    def test