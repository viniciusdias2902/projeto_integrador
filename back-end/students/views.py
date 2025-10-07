from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Student
from .serializers import StudentSerializer, StudentCreateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from common.permissions import GlobalDefaultPermission


class StudentListCreateView(ListCreateAPIView):
    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return StudentCreateSerializer
        return StudentSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated(), GlobalDefaultPermission()]


class StudentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
