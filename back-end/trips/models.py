from django.db import models
from django.utils import timezone
from boarding_points.models import BoardingPoint
from polls.models import Poll


TRIP_TYPE_CHOICES = (
    ("outbound", "Outbound"),
    ("return", "Return"),
)

TRIP_STATUS_CHOICES = (
    ("pending", "Pending"),
    ("in_progress", "In Progress"),
    ("completed", "Completed"),
)

UNIVERSITY_ORDER = {
    "IFPI": 0,
    "CHRISFAPI": 1,
    "UESPI": 2,
    "ETC": 3,
}


class Trip(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="trips")
    trip_type = models.CharField(max_length=20, choices=TRIP_TYPE_CHOICES)
    status = models.CharField(
        max_length=20, choices=TRIP_STATUS_CHOICES, default="pending"
    )
    current_boarding_point = models.ForeignKey(
        BoardingPoint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="current_trips",
    )
    current_university = models.CharField(max_length=50, null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("poll", "trip_type")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Trip {self.trip_type} for {self.poll.date} - {self.status}"

    def start_trip(self):
        if self.status != "pending":
            raise ValueError("Trip already started or completed")

        if self.trip_type == "outbound":
            points = self.get_boarding_points()
            if not points:
                raise ValueError("No boarding points for this trip")

            first_point = points[0]
            self.status = "in_progress"
            self.current_boarding_point = first_point
            self.started_at = timezone.now()
            self.save()
            return first_point
        else:
            universities = self.get_universities()
            if not universities:
                raise ValueError("No universities for this trip")

            first_university = universities[0]
            self.status = "in_progress"
            self.current_university = first_university
            self.started_at = timezone.now()
            self.save()
            return first_university

    def next_stop(self):
        if self.status != "in_progress":
            raise ValueError("Trip is not in progress")

        if self.trip_type == "outbound":
            return self._next_boarding_point()
        else:
            return self._next_university()

    def _next_boarding_point(self):
        if not self.current_boarding_point:
            raise ValueError("No current boarding point")

        boarding_points = list(self.get_boarding_points())
        current_index = next(
            (
                i
                for i, bp in enumerate(boarding_points)
                if bp.id == self.current_boarding_point.id
            ),
            None,
        )

        if current_index is None:
            raise ValueError("Current boarding point not found")

        if current_index + 1 < len(boarding_points):
            next_point = boarding_points[current_index + 1]
            self.current_boarding_point = next_point
            self.save()
            return next_point
        else:
            self.complete_trip()
            return None

    def _next_university(self):
        if not self.current_university:
            raise ValueError("No current university")

        universities = self.get_universities()
        current_index = universities.index(self.current_university)

        if current_index + 1 < len(universities):
            next_university = universities[current_index + 1]
            self.current_university = next_university
            self.save()
            return next_university
        else:
            self.complete_trip()
            return None

    def complete_trip(self):
        if self.status != "in_progress":
            raise ValueError("Trip is not in progress")

        self.status = "completed"
        self.completed_at = timezone.now()
        self.current_boarding_point = None
        self.current_university = None
        self.save()

    def get_boarding_points(self):
        if self.trip_type != "outbound":
            return []

        valid_options = ["round_trip", "one_way_outbound"]
        votes = self.poll.votes.filter(option__in=valid_options).select_related(
            "student__boarding_point"
        )

        point_ids = set()
        for vote in votes:
            if vote.student.boarding_point:
                point_ids.add(vote.student.boarding_point.id)

        return list(
            BoardingPoint.objects.filter(id__in=point_ids).order_by("route_order")
        )

    def get_universities(self):
        if self.trip_type != "return":
            return []

        valid_options = ["round_trip", "one_way_return"]
        votes = self.poll.votes.filter(option__in=valid_options).select_related(
            "student"
        )

        university_set = set()
        for vote in votes:
            university_set.add(vote.student.university)

        universities = sorted(
            university_set, key=lambda u: UNIVERSITY_ORDER.get(u, 999)
        )
        return universities

    def get_students_at_point(self, boarding_point):
        if self.trip_type != "outbound":
            return []

        valid_options = ["round_trip", "one_way_outbound"]
        votes = self.poll.votes.filter(
            option__in=valid_options, student__boarding_point=boarding_point
        ).select_related("student")

        return [vote.student for vote in votes]

    def get_students_at_university(self, university):
        if self.trip_type != "return":
            return []

        valid_options = ["round_trip", "one_way_return"]
        votes = self.poll.votes.filter(
            option__in=valid_options, student__university=university
        ).select_related("student")

        students = [vote.student for vote in votes]
        return sorted(students, key=lambda s: s.name)

    def get_current_students(self):
        if self.trip_type == "outbound" and self.current_boarding_point:
            return self.get_students_at_point(self.current_boarding_point)
        elif self.trip_type == "return" and self.current_university:
            return self.get_students_at_university(self.current_university)
        return []
