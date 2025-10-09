from rest_framework import viewsets, permissions
from .models import BoardingPoint
from .serializers import BoardingPointSerializer


class BoardingPointViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows boarding points to be viewed or edited.
    """

    queryset = BoardingPoint.objects.all()
    serializer_class = BoardingPointSerializer
