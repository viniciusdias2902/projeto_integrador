from rest_framework import viewsets, permissions
from .models import BoardingPoint
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import BoardingPointSerializer
from common.permissions import GlobalDefaultPermission


class BoardingPointViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows boarding points to be viewed or edited.
    """

    queryset = BoardingPoint.objects.all()
    serializer_class = BoardingPointSerializer
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)

    def get_permissions(self):
     if self.request.method in ["GET", "HEAD", "OPTIONS"]:
        return [AllowAny()]
     return [IsAuthenticated(), GlobalDefaultPermission()]
