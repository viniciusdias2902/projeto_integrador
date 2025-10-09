from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import IntegrityError, transaction
from django.utils import timezone
from .models import Poll, Vote
from .serializers import PollSerializer, VoteSerializer, BoardingListSerializer
from boarding_points.models import BoardingPoint

from datetime import date, timedelta


class PollListView(generics.ListAPIView):
    queryset = Poll.objects.all().order_by("date")
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticated]


class PollDetailView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticated]


class PollBoardingListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        poll = generics.get_object_or_404(Poll, pk=pk)

        trip_type = request.query_params.get("trip_type")
        if not trip_type:
            return Response(
                {
                    "error": "O parâmetro 'trip_type' é obrigatório (ex: outbound, return)."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_options = []
        if "outbound" in trip_type:
            valid_options = ["round_trip", "one_way_outbound"]
        elif "return" in trip_type:
            valid_options = ["round_trip", "one_way_return"]

        votes = poll.votes.filter(option__in=valid_options).select_related(
            "student", "student__boarding_point"
        )

        if "return" in trip_type:

            university_order = {
                "IFPI": 0,
                "CHRISFAPI": 1,
                "UESPI": 2,
                "ETC": 3,
            }

            university_data = {}
            for vote in votes:
                student = vote.student
                university = student.university

                if university not in university_data:
                    university_data[university] = {
                        "university": university,
                        "students": [],
                    }
                university_data[university]["students"].append(student)

            sorted_universities = sorted(
                university_data.values(),
                key=lambda u: university_order.get(u["university"], 999),
            )

            for uni_data in sorted_universities:
                uni_data["students"].sort(key=lambda s: s.name)

            result = []
            for uni_data in sorted_universities:
                result.append(
                    {
                        "group_name": uni_data["university"],
                        "group_type": "university",
                        "students": [
                            {"id": s.id, "name": s.name} for s in uni_data["students"]
                        ],
                    }
                )

            return Response(result)
        else:

            points_data = {}
            for vote in votes:
                point = vote.student.boarding_point
                if point:
                    if point.id not in points_data:
                        points_data[point.id] = {
                            "boarding_point": point,
                            "students": [],
                        }
                    points_data[point.id]["students"].append(vote.student)

            sorted_points = sorted(
                points_data.values(), key=lambda p: p["boarding_point"].route_order
            )

            serializer = BoardingListSerializer(sorted_points, many=True)
            return Response(serializer.data)


class CreateWeeklyPollsView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        created_polls = []
        today = timezone.localtime(timezone.now()).date()

        weekday = today.weekday()

        if weekday == 5:
            start_date = today + timedelta(days=2)
        elif weekday == 6:
            start_date = today + timedelta(days=1)
        else:
            start_date = today

        current_date = start_date
        while current_date.weekday() <= 4:
            poll, created = Poll.objects.get_or_create(
                date=current_date, defaults={"status": "open"}
            )
            if created:
                created_polls.append(str(current_date))

            current_date += timedelta(days=1)

        return Response(
            {
                "message": "Enquetes criadas com sucesso",
                "created_polls": created_polls,
                "total": len(created_polls),
            }
        )


class CleanOldPollsView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        today = timezone.localtime(timezone.now()).date()

        deleted_polls = Poll.objects.filter(date__lt=today)
        count = deleted_polls.count()
        deleted_dates = list(deleted_polls.values_list("date", flat=True))
        deleted_polls.delete()

        return Response(
            {
                "message": "Enquetes antigas removidas com sucesso",
                "deleted_count": count,
                "deleted_dates": [str(d) for d in deleted_dates],
            }
        )


class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        poll = serializer.validated_data["poll"]
        option = serializer.validated_data["option"]

        if not poll.can_vote_for_option(option):
            if option in ["round_trip", "one_way_outbound"]:
                raise serializers.ValidationError(
                    "O prazo para votar em 'Ida e Volta' ou 'Apenas Ida' é até 12:00 do dia da enquete."
                )
            else:
                raise serializers.ValidationError(
                    "O prazo para votar em 'Apenas Volta' ou 'Não Vou' é até 18:00 do dia da enquete."
                )

        serializer.save(student=self.request.user.student)

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"detail": "Você já votou nesta enquete."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class VoteListView(generics.ListAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.filter(student=self.request.user.student)


class VoteUpdateView(generics.UpdateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.filter(student=self.request.user.student)

    def perform_update(self, serializer):
        poll = serializer.instance.poll
        option = serializer.validated_data.get("option", serializer.instance.option)

        if not poll.can_vote_for_option(option):
            if option in ["round_trip", "one_way_outbound"]:
                raise serializers.ValidationError(
                    "O prazo para votar em 'Ida e Volta' ou 'Apenas Ida' é até 12:00 do dia da enquete."
                )
            else:
                raise serializers.ValidationError(
                    "O prazo para votar em 'Apenas Volta' ou 'Não Vou' é até 18:00 do dia da enquete."
                )

        serializer.save()
