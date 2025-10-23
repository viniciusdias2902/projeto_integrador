from rest_framework import serializers
from .models import Trip, UNIVERSITY_ORDER
from boarding_points.serializers import BoardingPointSerializer
from polls.serializers import StudentNestedSerializer


UNIVERSITY_NAMES = {
    "IFPI": "Instituto Federal do Piaui",
    "CHRISFAPI": "Christus Faculdade do Piaui",
    "UESPI": "Universidade Estadual do Piaui",
    "ETC": "Other",
}


class TripSerializer(serializers.ModelSerializer):
    current_boarding_point = BoardingPointSerializer(read_only=True)
    current_university_name = serializers.SerializerMethodField()
    total_stops = serializers.SerializerMethodField()
    current_stop_index = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = [
            "id",
            "poll",
            "trip_type",
            "status",
            "current_boarding_point",
            "current_university",
            "current_university_name",
            "total_stops",
            "current_stop_index",
            "started_at",
            "completed_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "current_boarding_point",
            "current_university",
            "started_at",
            "completed_at",
            "created_at",
        ]

    def get_current_university_name(self, obj):
        if obj.current_university:
            return UNIVERSITY_NAMES.get(obj.current_university, obj.current_university)
        return None

    def get_total_stops(self, obj):
        if obj.trip_type == "outbound":
            return len(obj.get_boarding_points())
        else:
            return len(obj.get_universities())

    def get_current_stop_index(self, obj):
        if obj.status != "in_progress":
            return None

        if obj.trip_type == "outbound":
            if not obj.current_boarding_point:
                return None
            boarding_points = obj.get_boarding_points()
            for i, bp in enumerate(boarding_points):
                if bp.id == obj.current_boarding_point.id:
                    return i
        else:
            if not obj.current_university:
                return None
            universities = obj.get_universities()
            try:
                return universities.index(obj.current_university)
            except ValueError:
                return None

        return None


class TripDetailSerializer(TripSerializer):
    stops = serializers.SerializerMethodField()

    class Meta(TripSerializer.Meta):
        fields = TripSerializer.Meta.fields + ["stops"]

    def get_stops(self, obj):
        if obj.trip_type == "outbound":
            points = obj.get_boarding_points()
            result = []

            for point in points:
                students = obj.get_students_at_point(point)
                result.append(
                    {
                        "boarding_point": BoardingPointSerializer(point).data,
                        "students": StudentNestedSerializer(students, many=True).data,
                        "student_count": len(students),
                        "is_current": (
                            obj.current_boarding_point
                            and obj.current_boarding_point.id == point.id
                        ),
                    }
                )

            return result
        else:
            universities = obj.get_universities()
            result = []

            for university in universities:
                students = obj.get_students_at_university(university)
                result.append(
                    {
                        "university": university,
                        "university_name": UNIVERSITY_NAMES.get(university, university),
                        "students": StudentNestedSerializer(students, many=True).data,
                        "student_count": len(students),
                        "is_current": obj.current_university == university,
                    }
                )

            return result
