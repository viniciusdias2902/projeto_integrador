from rest_framework import viewsets, permissions
from .models import BoardingPoint
from rest_framework.permissions import IsAuthenticated
from .serializers import BoardingPointSerializer
from common.permissions import GlobalDefaultPermission


class BoardingPointViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows boarding points to be viewed or edited.
    """

    queryset = BoardingPoint.objects.all()
    serializer_class = BoardingPointSerializer
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
