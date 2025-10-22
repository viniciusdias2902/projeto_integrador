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
                f"Já existe uma viagem do tipo '{trip_type}' para esta enquete."
            )

        serializer.save()


class TripStartView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        trip = get_object_or_404(Trip, pk=pk)

        try:
            first_point = trip.start_trip()
            students = trip.get_students_at_point(first_point)

            return Response(
                {
                    "message": "Viagem iniciada com sucesso",
                    "trip": TripSerializer(trip).data,
                    "current_boarding_point": BoardingPointSerializer(first_point).data,
                    "students": StudentNestedSerializer(students, many=True).data,
                    "student_count": len(students),
                }
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TripNextPointView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        trip = get_object_or_404(Trip, pk=pk)

        try:
            next_point = trip.next_boarding_point()

            if next_point is None:
                # Viagem finalizada
                return Response(
                    {
                        "message": "Viagem finalizada com sucesso",
                        "trip": TripSerializer(trip).data,
                        "completed": True,
                    }
                )
            else:
                # Próximo ponto
                students = trip.get_students_at_point(next_point)
                return Response(
                    {
                        "message": "Avançado para o próximo ponto",
                        "trip": TripSerializer(trip).data,
                        "current_boarding_point": BoardingPointSerializer(
                            next_point
                        ).data,
                        "students": StudentNestedSerializer(students, many=True).data,
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
            return Response(
                {
                    "message": "Viagem finalizada com sucesso",
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

        if trip.current_boarding_point and trip.status == "in_progress":
            students = trip.get_students_at_point(trip.current_boarding_point)
            response_data["current_students"] = StudentNestedSerializer(
                students, many=True
            ).data
            response_data["current_student_count"] = len(students)

        return Response(response_data)
