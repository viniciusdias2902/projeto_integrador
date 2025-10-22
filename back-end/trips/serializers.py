from rest_framework import serializers
from .models import Trip
from boarding_points.serializers import BoardingPointSerializer
from polls.serializers import StudentNestedSerializer


class TripSerializer(serializers.ModelSerializer):
    current_boarding_point = BoardingPointSerializer(read_only=True)
    total_boarding_points = serializers.SerializerMethodField()
    current_point_index = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = [
            "id",
            "poll",
            "trip_type",
            "status",
            "current_boarding_point",
            "total_boarding_points",
            "current_point_index",
            "started_at",
            "completed_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "current_boarding_point",
            "started_at",
            "completed_at",
            "created_at",
        ]

    def get_total_boarding_points(self, obj):
        return obj.get_boarding_points().count()

    def get_current_point_index(self, obj):
        if not obj.current_boarding_point or obj.status != "in_progress":
            return None

        boarding_points = list(obj.get_boarding_points())
        for i, bp in enumerate(boarding_points):
            if bp.id == obj.current_boarding_point.id:
                return i
        return None


class TripDetailSerializer(TripSerializer):
    boarding_points = serializers.SerializerMethodField()

    class Meta(TripSerializer.Meta):
        fields = TripSerializer.Meta.fields + ["boarding_points"]

    def get_boarding_points(self, obj):
        points = obj.get_boarding_points()
        result = []

        for point in points:
            students = obj.get_students_at_point(point)
            result.append(
                {
                    "boarding_point": BoardingPointSerializer(point).data,
                    "students": StudentNestedSerializer(students, many=True).data,
                    "student_count": len(students),
                    "is_current": obj.current_boarding_point
                    and obj.current_boarding_point.id == point.id,
                }
            )

        return result
