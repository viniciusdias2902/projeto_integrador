# polls/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Poll, Vote
from .serializers import PollSerializer, VoteSerializer


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


class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student)


# Lista votos do aluno logado
class VoteListView(generics.ListAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.filter(student=self.request.user.student)
