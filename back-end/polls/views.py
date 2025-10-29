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
            # Para VOLTA: agrupar por universidade
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

            # Ordenar universidades
            sorted_universities = sorted(
                university_data.values(),
                key=lambda u: university_order.get(u["university"], 999),
            )

            # Ordenar estudantes dentro de cada universidade por nome
            for uni_data in sorted_universities:
                uni_data["students"].sort(key=lambda s: s.name)

            # Serializar de forma consistente
            result = []
            for uni_data in sorted_universities:
                result.append(
                    {
                        "group_name": uni_data["university"],
                        "students": [
                            {"id": s.id, "name": s.name} for s in uni_data["students"]
                        ],
                    }
                )

            return Response(result)
        else:
            # Para IDA: agrupar por ponto de embarque
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

            # Serializar de forma consistente com a volta
            result = []
            for point_data in sorted_points:
                point = point_data["boarding_point"]
                result.append(
                    {
                        "point": {
                            "id": point.id,
                            "name": point.name,
                            "address_reference": point.address_reference,
                        },
                        "students": [
                            {"id": s.id, "name": s.name} for s in point_data["students"]
                        ],
                    }
                )

            return Response(result)


class CreateWeeklyPollsView(APIView):
    """
    Cria enquetes para os dias restantes da semana atual.
    - Se chamado na segunda: cria segunda a sexta
    - Se chamado na quarta: cria quarta, quinta e sexta
    - Se chamado no sábado: cria segunda a sexta da próxima semana
    - Se chamado no domingo: cria segunda a sexta da próxima semana
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        created_polls = []
        existing_polls = []
        today = timezone.localtime(timezone.now()).date()

        weekday = today.weekday()  # 0=Monday, 6=Sunday

        # Determinar data de início baseado no dia da semana
        if weekday == 5:  # Sábado
            start_date = today + timedelta(days=2)  # Próxima segunda
        elif weekday == 6:  # Domingo
            start_date = today + timedelta(days=1)  # Próxima segunda
        else:  # Segunda a sexta
            start_date = today  # Começa hoje

        # Determinar data de fim (sexta-feira da mesma semana)
        end_date = start_date
        while end_date.weekday() < 4:  # Avançar até sexta (weekday = 4)
            end_date += timedelta(days=1)

        # Criar enquetes do start_date até end_date
        current_date = start_date
        while current_date <= end_date:
            poll, created = Poll.objects.get_or_create(
                date=current_date, defaults={"status": "open"}
            )

            if created:
                created_polls.append(str(current_date))
            else:
                existing_polls.append(str(current_date))

            current_date += timedelta(days=1)

        return Response(
            {
                "message": "Processo de criação de enquetes concluído",
                "created_polls": created_polls,
                "existing_polls": existing_polls,
                "total_created": len(created_polls),
                "total_existing": len(existing_polls),
                "start_date": str(start_date),
                "end_date": str(end_date),
                "today": str(today),
                "weekday": weekday,
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
        # Valida se o horário permite votar na opção escolhida
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
