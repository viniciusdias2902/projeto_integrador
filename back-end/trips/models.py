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
            raise ValueError("A viagem já foi iniciada ou concluída.")

        first_point = self.get_boarding_points().first()

        if not first_point:
            raise ValueError("Não há pontos de embarque para esta viagem.")

        self.status = "in_progress"
        self.current_boarding_point = first_point
        self.started_at = timezone.now()
        self.save()

        return first_point

    def next_boarding_point(self):

        if self.status != "in_progress":
            raise ValueError("A viagem não está em andamento.")

        if not self.current_boarding_point:
            raise ValueError("Não há ponto atual definido.")

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
            raise ValueError("Ponto atual não encontrado na lista de pontos.")

        if current_index + 1 < len(boarding_points):
            next_point = boarding_points[current_index + 1]
            self.current_boarding_point = next_point
            self.save()
            return next_point
        else:

            self.complete_trip()
            return None

    def complete_trip(self):

        if self.status != "in_progress":
            raise ValueError("A viagem não está em andamento.")

        self.status = "completed"
        self.completed_at = timezone.now()
        self.current_boarding_point = None
        self.save()

    def get_boarding_points(self):

        if self.trip_type == "outbound":
            valid_options = ["round_trip", "one_way_outbound"]
        else:
            valid_options = ["round_trip", "one_way_return"]

        votes = self.poll.votes.filter(option__in=valid_options).select_related(
            "student__boarding_point"
        )

        point_ids = set()
        for vote in votes:
            if vote.student.boarding_point:
                point_ids.add(vote.student.boarding_point.id)

        return BoardingPoint.objects.filter(id__in=point_ids).order_by("route_order")

    def get_students_at_point(self, boarding_point):

        if self.trip_type == "outbound":
            valid_options = ["round_trip", "one_way_outbound"]
        else:
            valid_options = ["round_trip", "one_way_return"]

        votes = self.poll.votes.filter(
            option__in=valid_options, student__boarding_point=boarding_point
        ).select_related("student")

        return [vote.student for vote in votes]
