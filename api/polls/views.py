from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import IntegrityError, transaction
from .models import Poll, Vote
from .serializers import PollSerializer, VoteSerializer
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
        votes = poll.votes.select_related("student").all()
        data = [{"student": v.student.user.username, "option": v.option} for v in votes]
        return Response(data)


class CreateTestPollsView(APIView):
    """
    Create 5 consecutive polls starting from today.
    Only for testing purposes.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        created_polls = []
        today = date.today()

        for i in range(5):
            poll_date = today + timedelta(days=i)
            poll, created = Poll.objects.get_or_create(
                date=poll_date, defaults={"status": "open"}
            )
            if created:
                created_polls.append(str(poll_date))

        return Response(
            {"message": "Polls successfully created", "created_polls": created_polls}
        )


class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student)
    
    def create(self, request, *args):
        try:
            with transaction.atomic():
                return super().create(request, *args)
        except IntegrityError:
            return Response(
                {"detail": "Você já votou nesta enquete."},
                status=status.HTTP_400_BAD_REQUEST
            )



class VoteListView(generics.ListAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.filter(student=self.request.user.student)


class PollBoardingListView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        poll = generics.get_object_or_404(Poll, pk=pk)
        students = poll.votes.select_related("student").all()
        student_names = [v.student.name for v in students]
        boarding_list = ", ".join(student_names)
        return Response({"boarding_list": boarding_list})
