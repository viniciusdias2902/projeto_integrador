from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Trip
from .serializers import TripSerializer, TripDetailSerializer
from polls.models import Poll
from boarding_points.serializers import BoardingPointSerializer
from polls.serializers import StudentNestedSerializer


class TripListView(generics.ListAPIView):
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Trip.objects.all()
        poll_id = self.request.query_params.get("poll_id")
        trip_type = self.request.query_params.get("trip_type")
        trip_status = self.request.query_params.get("status")

        if poll_id:
            queryset = queryset.filter(poll_id=poll_id)
        if trip_type:
            queryset = queryset.filter(trip_type=trip_type)
        if trip_status:
            queryset = queryset.filter(status=trip_status)

        return queryset


class TripDetailView(generics.RetrieveAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class TripCreateView(generics.CreateAPIView):
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        poll = serializer.validated_data["poll"]
        trip_type = serializer.validated_data["trip_type"]

        if Trip.objects.filter(poll=poll, trip_type=trip_type).exists():
            raise serializers.ValidationError(
                f"Trip of type '{trip_type}' already exists for this poll"
            )

        serializer.save()


class TripStartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        trip = get_object_or_404(Trip, pk=pk)

        try:
            result = trip.start_trip()

            if trip.trip_type == "outbound":
                students = trip.get_students_at_point(result)
                return Response(
                    {
                        "message": "Outbound trip started",
                        "trip": TripSerializer(trip).data,
                        "current_boarding_point": BoardingPointSerializer(result).data,
                        "students": StudentNestedSerializer(students, many=True).data,
                        "student_count": len(students),
                    }
                )
            else:
                students = trip.get_students_at_university(result)
                return Response(
                    {
                        "message": "Return trip started",
                        "trip": TripSerializer(trip).data,
                        "current_university": result,
                        "students": StudentNestedSerializer(students, many=True).data,
                        "student_count": len(students),
                    }
                )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TripNextStopView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        trip = get_object_or_404(Trip, pk=pk)

        try:
            next_stop = trip.next_stop()

            if next_stop is None:
                if trip.trip_type == "outbound":
                    return_trip, created = Trip.objects.get_or_create(
                        poll=trip.poll,
                        trip_type="return",
                        defaults={"status": "pending"},
                    )

                    return Response(
                        {
                            "message": "Outbound trip completed, return trip ready",
                            "trip": TripSerializer(trip).data,
                            "return_trip": TripSerializer(return_trip).data,
                            "completed": True,
                        }
                    )
                else:
                    return Response(
                        {
                            "message": "Return trip completed",
                            "trip": TripSerializer(trip).data,
                            "completed": True,
                        }
                    )
            else:
                if trip.trip_type == "outbound":
                    students = trip.get_students_at_point(next_stop)
                    return Response(
                        {
                            "message": "Moved to next stop",
                            "trip": TripSerializer(trip).data,
                            "current_boarding_point": BoardingPointSerializer(
                                next_stop
                            ).data,
                            "students": StudentNestedSerializer(
                                students, many=True
                            ).data,
                            "student_count": len(students),
                            "completed": False,
                        }
                    )
                else:
                    students = trip.get_students_at_university(next_stop)
                    return Response(
                        {
                            "message": "Moved to next university",
                            "trip": TripSerializer(trip).data,
                            "current_university": next_stop,
                            "students": StudentNestedSerializer(
                                students, many=True
                            ).data,
                            "student_count": len(students),
                            "completed": False,
                        }
                    )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TripCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        trip = get_object_or_404(Trip, pk=pk)

        try:
            trip.complete_trip()

            if trip.trip_type == "outbound":
                return_trip, created = Trip.objects.get_or_create(
                    poll=trip.poll, trip_type="return", defaults={"status": "pending"}
                )

                return Response(
                    {
                        "message": "Outbound trip completed manually, return trip ready",
                        "trip": TripSerializer(trip).data,
                        "return_trip": TripSerializer(return_trip).data,
                    }
                )
            else:
                return Response(
                    {
                        "message": "Return trip completed",
                        "trip": TripSerializer(trip).data,
                    }
                )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TripCurrentStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        trip = get_object_or_404(Trip, pk=pk)

        response_data = {
            "trip": TripDetailSerializer(trip).data,
        }

        if trip.status == "in_progress":
            students = trip.get_current_students()
            response_data["current_students"] = StudentNestedSerializer(
                students, many=True
            ).data
            response_data["current_student_count"] = len(students)

        return Response(response_data)
