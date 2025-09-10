from django.db import models

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


class Vote(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    poll = models.ForeignKey("Poll", on_delete=models.CASCADE, related_name="votes")
    option = models.CharField(
        max_length=20,
        choices=OPTIONS,
    )

    class Meta:
        unique_together = ("student", "poll")

    def __str__(self):
        return f"{self.student} - {self.poll.date} - {self.option}"
