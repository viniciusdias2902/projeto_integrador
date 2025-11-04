from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Admin
from .serializers import AdminSerializer, AdminCreateSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from common.permissions import GlobalDefaultPermission


class AdminListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = Admin.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AdminCreateSerializer
        return AdminSerializer


class AdminRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
