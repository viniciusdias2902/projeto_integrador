from django.test import TestCase
from django.core.management import call_command
from django.utils import timezone
from datetime import timedelta, date
from unittest.mock import patch
from io import StringIO
from polls.models import Poll


class CreateWeeklyPollsCronTests(TestCase):

    @patch("django.utils.timezone.now")
    def test_creates_polls_for_next_week_on_saturday(self, mock_now):
        saturday = date(2025, 11, 29)
        mock_now.return_value = timezone.make_aware(
            timezone.datetime.combine(saturday, timezone.datetime.min.time())
        )

        out = StringIO()
        call_command("create_weekly_polls_cron", stdout=out)

        self.assertEqual(Poll.objects.count(), 5)

        next_monday = date(2025, 12, 1)
        for i in range(5):
            poll_date = next_monday + timedelta(days=i)
            self.assertTrue(Poll.objects.filter(date=poll_date).exists())

    @patch("django.utils.timezone.now")
    def test_removes_old_polls_on_saturday(self, mock_now):
        saturday = date(2025, 11, 29)
        mock_now.return_value = timezone.make_aware(
            timezone.datetime.combine(saturday, timezone.datetime.min.time())
        )

        old_poll = Poll.objects.create(date=date(2025, 11, 28))

        out = StringIO()
        call_command("create_weekly_polls_cron", stdout=out)

        self.assertFalse(Poll.objects.filter(id=old_poll.id).exists())

    @patch("django.utils.timezone.now")
    def test_does_not_create_duplicate_polls(self, mock_now):
        saturday = date(2025, 11, 29)
        mock_now.return_value = timezone.make_aware(
            timezone.datetime.combine(saturday, timezone.datetime.min.time())
        )

        next_monday = date(2025, 12, 1)
        Poll.objects.create(date=next_monday)

        out = StringIO()
        call_command("create_weekly_polls_cron", stdout=out)

        self.assertEqual(Poll.objects.filter(date=next_monday).count(), 1)

    @patch("django.utils.timezone.now")
    def test_warning_when_not_saturday(self, mock_now):
        monday = date(2025, 11, 24)
        mock_now.return_value = timezone.make_aware(
            timezone.datetime.combine(monday, timezone.datetime.min.time())
        )

        out = StringIO()
        call_command("create_weekly_polls_cron", stdout=out)

        self.assertIn("should only run on Saturdays", out.getvalue())


class CleanYesterdayPollTests(TestCase):

    @patch("django.utils.timezone.now")
    def test_removes_yesterday_poll_on_tuesday(self, mock_now):
        tuesday = date(2025, 11, 25)
        mock_now.return_value = timezone.make_aware(
            timezone.datetime.combine(tuesday, timezone.datetime.min.time())
        )

        monday = date(2025, 11, 24)
        monday_poll = Poll.objects.create(date=monday)

        out = StringIO()
        call_command("clean_yesterday_poll", stdout=out)

        self.assertFalse(Poll.objects.filter(id=monday_poll.id).exists())
        self.assertIn(f"Deleted poll for date: {monday}", out.getvalue())

    @patch("django.utils.timezone.now")
    def test_removes_yesterday_poll_on_wednesday(self, mock_now):
        wednesday = date(2025, 11, 26)
        mock_now.return_value = timezone.make_aware(
            timezone.datetime.combine(wednesday, timezone.datetime.min.time())
        )

        tuesday = date(2025, 11, 25)
        tuesday_poll = Poll.objects.create(date=tuesday)

        out = StringIO()
        call_command("clean_yesterday_poll", stdout=out)

        self.assertFalse(Poll.objects.filter(id=tuesday_poll.id).exists())

    @patch("django.utils.timezone.now")
    def test_removes_yesterday_poll_on_thursday(self, mock_now):
        thursday = date(2025, 11, 27)
        mock_now.return_value = timezone.make_aware(
            timezone.datetime.combine(thursday, timezone.datetime.min.time())
        )

        wednesday = date(2025, 11, 26)
        wednesday_poll = Poll.objects.create(date=wednesday)

        out = StringIO()
        call_command("clean_yesterday_poll", stdout=out)

        self.assertFalse(Poll.objects.filter(id=wednesday_poll.id).exists())

    @patch("django.utils.timezone.now")
    def test_removes_yesterday_poll_on_friday(self, mock_now):
        friday = date(2025, 11, 28)
        mock_now.return_value = timezone.make_aware(
            timezone.datetime.combine(friday, timezone.datetime.min.time())
        )

        thursday = date(2025, 11, 27)
        thursday_poll = Poll.objects.create(date=thursday)

        out = StringIO()
        call_command("clean_yesterday_poll", stdout=out)

        self.assertFalse(Poll.objects.filter(id=thursday_poll.id).exists())

    @patch("django.utils.timezone.now")
    def test_does_not_remove_today_poll(self, mock_now):
        tuesday = date(2025, 11, 25)
        mock_now.return_value = timezone.make_aware(
            timezone.datetime.combine(tuesday, timezone.datetime.min.time())
        )

        tuesday_poll = Poll.objects.create(date=tuesday)

        out = StringIO()
        call_command("clean_yesterday_poll", stdout=out)

        self.assertTrue(Poll.objects.filter(id=tuesday_poll.id).exists())

    @patch("django.utils.timezone.now")
    def test_does_not_remove_future_polls(self, mock_now):
        tuesday = date(2025, 11, 25)
        mock_now.return_value = timezone.make_aware(
            timezone.datetime.combine(tuesday, timezone.datetime.min.time())
        )

        wednesday_poll = Poll.objects.create(date=date(2025, 11, 26))

        out = StringIO()
        call_command("clean_yesterday_poll", stdout=out)

        self.assertTrue(Poll.objects.filter(id=wednesday_poll.id).exists())

    @patch("django.utils.timezone.now")
    def test_warning_when_run_on_monday(self, mock_now):
        monday = date(2025, 11, 24)
        mock_now.return_value = timezone.make_aware(
            timezone.datetime.combine(monday, timezone.datetime.min.time())
        )

        out = StringIO()
        call_command("clean_yesterday_poll", stdout=out)

        self.assertIn("should only run Tuesday to Friday", out.getvalue())

    @patch("django.utils.timezone.now")
    def test_warning_when_run_on_saturday(self, mock_now):
        saturday = date(2025, 11, 29)
        mock_now.return_value = timezone.make_aware(
            timezone.datetime.combine(saturday, timezone.datetime.min.time())
        )

        out = StringIO()
        call_command("clean_yesterday_poll", stdout=out)

        self.assertIn("should only run Tuesday to Friday", out.getvalue())

    @patch("django.utils.timezone.now")
    def test_warning_when_run_on_sunday(self, mock_now):
        sunday = date(2025, 11, 30)
        mock_now.return_value = timezone.make_aware(
            timezone.datetime.combine(sunday, timezone.datetime.min.time())
        )

        out = StringIO()
        call_command("clean_yesterday_poll", stdout=out)

        self.assertIn("should only run Tuesday to Friday", out.getvalue())

    @patch("django.utils.timezone.now")
    def test_handles_no_poll_for_yesterday(self, mock_now):
        tuesday = date(2025, 11, 25)
        mock_now.return_value = timezone.make_aware(
            timezone.datetime.combine(tuesday, timezone.datetime.min.time())
        )

        out = StringIO()
        call_command("clean_yesterday_poll", stdout=out)

        monday = date(2025, 11, 24)
        self.assertIn(f"No poll found for date: {monday}", out.getvalue())