# polls/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Poll, Vote
from .serializers import PollSerializer, VoteSerializer


# Lista todas as enquetes
class PollListView(generics.ListAPIView):
    queryset = Poll.objects.all().order_by("date")
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticated]


# Detalhe de uma enquete específica
class PollDetailView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticated]


# Lista de embarque para motoristas
class PollBoardingListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        poll = generics.get_object_or_404(Poll, pk=pk)
        votes = poll.votes.select_related("student").all()
        data = [{"student": v.student.user.username, "option": v.option} for v in votes]
        return Response(data)
