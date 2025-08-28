from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Driver
from .serializers import DriverSerializer, DriverCreateSerializer


class DriverListCreateView(ListCreateAPIView):
    queryset = Driver.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return DriverCreateSerializer
        return DriverSerializer


class DriverRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
