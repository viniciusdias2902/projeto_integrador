from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Driver
from .serializers import DriverSerializer, DriverCreateSerializer
from rest_framework.permissions import IsAuthenticated
from common.permissions import GlobalDefaultPermission


class DriverListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = Driver.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return DriverCreateSerializer
        return DriverSerializer


class DriverRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
