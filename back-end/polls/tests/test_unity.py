from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError
from datetime import date, timedelta, datetime, time
from unittest.mock import patch, MagicMock
from rest_framework.test import APIRequestFactory, force_authenticate

from polls.models import Poll, Vote
from polls.views import (
    PollDetailView,
    PollListView,
    CreateWeeklyPollsView,
    CleanOldPollsView,
    VoteListView,
)
from students.models import Student
from polls.serializers import StudentNestedSerializer
from boarding_points.models import BoardingPoint


class PollModelLogicTests(TestCase):
    def setUp(self):
        self.today = timezone.localdate()
        self.poll_today = Poll.objects.create(date=self.today)
        self.poll_yesterday = Poll.objects.create(date=self.today - timedelta(days=1))
        self.poll_tomorrow = Poll.objects.create(date=self.today + timedelta(days=1))

    # Funcionalidade 1
    def test_CT_01_str_method(self):
        fixed_date = date(2025, 8, 14)
        poll = Poll.objects.create(date=fixed_date, status="open")
        self.assertEqual(str(poll), "Poll for 2025-08-14 (open)")

    # Funcionalidade 3
    def test_CT_04_cannot_vote_on_past_poll(self):
        fake_time = datetime.combine(self.today, time(10, 0))
        with patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = timezone.make_aware(fake_time)

            self.assertFalse(
                self.poll_yesterday.can_vote_for_option("one_way_outbound")
            )

    # Funcionalidade 3
    def test_CT_05_can_vote_on_future_poll(self):
        fake_time = datetime.combine(self.today, time(10, 0))
        with patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = timezone.make_aware(fake_time)

            self.assertTrue(self.poll_tomorrow.can_vote_for_option("round_trip"))

    # Funcionalidade 3
    def test_CT_06_morning_deadline_boundary(self):
        # liimite (12:00:00) -> passa
        fake_limit = datetime.combine(self.today, time(12, 0))
        with patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = timezone.make_aware(fake_limit)
            self.assertTrue(self.poll_today.can_vote_for_option("round_trip"))
            self.assertTrue(self.poll_today.can_vote_for_option("one_way_outbound"))

        # tempo expirado (12:01:00) -> falha
        fake_expired = datetime.combine(self.today, time(12, 1))
        with patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = timezone.make_aware(fake_expired)
            self.assertFalse(self.poll_today.can_vote_for_option("round_trip"))
            self.assertFalse(self.poll_today.can_vote_for_option("one_way_outbound"))

    # Funcionalidade 3
    def test_CT_07_afternoon_deadline_boundary(self):
        # limite (18:00:00) -> passa
        fake_limit = datetime.combine(self.today, time(18, 0))
        with patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = timezone.make_aware(fake_limit)
            self.assertTrue(self.poll_today.can_vote_for_option("one_way_return"))
            self.assertTrue(self.poll_today.can_vote_for_option("absent"))

        # tempo expirado (18:01:00) -> falha
        fake_expired = datetime.combine(self.today, time(18, 1))
        with patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = timezone.make_aware(fake_expired)
            self.assertFalse(self.poll_today.can_vote_for_option("one_way_return"))
            self.assertFalse(self.poll_today.can_vote_for_option("absent"))


class VoteModelIntegrityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="voter_user")
        bp = BoardingPoint.objects.create(name="Ponto Teste", route_order=1)

        self.student = Student.objects.create(
            name="Teste Votante",
            user=self.user,
            boarding_point=bp,
            class_shift="M",
            university="UESPI",
        )
        self.poll = Poll.objects.create(date=timezone.localdate())

    # Funcionalidade 2
    def test_CT_02_create_valid_vote(self):
        vote = Vote.objects.create(
            student=self.student, poll=self.poll, option="round_trip"
        )
        self.assertIsNotNone(vote.pk)
        self.assertEqual(vote.option, "round_trip")

    # Funcionalidade 2
    def test_CT_03_unique_vote_constraint(self):
        Vote.objects.create(student=self.student, poll=self.poll, option="round_trip")

        with self.assertRaises(IntegrityError):
            Vote.objects.create(student=self.student, poll=self.poll, option="absent")


class PollsSerializersTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="serializer_user")
        bp = BoardingPoint.objects.create(name="Ponto Serializer", route_order=1)
        self.student = Student.objects.create(
            name="Teste Serializer",
            user=self.user,
            boarding_point=bp,
            class_shift="M",
            university="UESPI",
        )

    # Funcionalidade 4
    def test_CT_08_student_nested_serializer_content(self):
        serializer = StudentNestedSerializer(self.student)
        data = serializer.data

        self.assertEqual(data["id"], self.student.id)
        self.assertEqual(data["name"], "Teste Serializer")
        self.assertEqual(data["user_id"], self.user.id)


class PollListViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PollListView.as_view()

    @patch("polls.views.Poll.objects")
    def test_CT_09_list_polls(self, mock_objects):
        request = self.factory.get("/polls/")
        force_authenticate(request, user=MagicMock())

        mock_objects.all.return_value.order_by.return_value = []

        response = self.view(request)
        self.assertEqual(response.status_code, 200)


class TestCreateWeeklyPollsView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CreateWeeklyPollsView.as_view()

    @patch("polls.views.timezone.now")
    @patch("polls.views.Poll.objects.get_or_create")
    def test_CT_10_create_weekly_polls(self, mock_get_or_create, mock_now):

        mock_now.return_value = timezone.make_aware(datetime(2025, 11, 26, 10, 0, 0))
        mock_get_or_create.return_value = (MagicMock(), True)
        request = self.factory.post("/polls/create_weekly/")
        force_authenticate(request, user=MagicMock())
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("created_polls", response.data)


class TestCleanOldPollsView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CleanOldPollsView.as_view()

    @patch("polls.views.timezone.now")
    @patch("polls.views.Poll.objects")
    def test_CT_11_clean_old_polls(self, mock_objects, mock_now):

        mock_now.return_value = timezone.make_aware(datetime(2025, 12, 1, 10, 0, 0))
        queryset = MagicMock()
        queryset.count.return_value = 2
        queryset.values_list.return_value = [date(2025, 11, 29), date(2025, 11, 30)]
        mock_objects.filter.return_value = queryset

        request = self.factory.post("/polls/clean_old/")
        force_authenticate(request, user=MagicMock())
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["deleted_count"], 2)


class TestVoteListView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = VoteListView.as_view()

    @patch("polls.views.Vote.objects")
    def test_CT_12_list_votes(self, mock_objects):
        mock_student = MagicMock()
        mock_student.id = 1
        mock_user = MagicMock()
        mock_user.student = mock_student
        mock_objects.filter.return_value = []

        request = self.factory.get("/votes/")
        force_authenticate(request, user=m)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

