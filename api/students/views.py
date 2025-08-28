from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Student
from .serializers import StudentSerializer, StudentCreateSerializer


class StudentListCreateView(ListCreateAPIView):
    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return StudentCreateSerializer
        return StudentSerializer


class StudentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
