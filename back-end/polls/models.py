from django.db import models
from django.utils import timezone
from datetime import time
from students.models import Student


STATUS = (("open", "Open"), ("closed", "Closed"))
OPTIONS = (
    ("round_trip", "Round Trip"),
    ("one_way_outbound", "Only Outbound"),
    ("one_way_return", "Only Return"),
    ("absent", "Absent"),
)


class Poll(models.Model):
    date = models.DateField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS, default="open")

    def __str__(self):
        return f"Poll for {self.date} ({self.status})"

    def can_vote_for_option(self, option):

        now = timezone.localtime(timezone.now())
        poll_date = self.date

        if now.date() < poll_date:
            return True

        if now.date() > poll_date:
            return False

        current_time = now.time()

        if option in ["round_trip", "one_way_outbound"]:
            return current_time <= time(12, 0)
        elif option in ["one_way_return", "absent"]:
            return current_time <= time(18, 0)

        return False


class Vote(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="votes")
    option = models.CharField(
        max_length=20,
        choices=OPTIONS,
    )
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "poll")

    def __str__(self):
        return f"{self.student} - {self.poll.date} - {self.option}"
