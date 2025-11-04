from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
    ListAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import (
    StudentSerializer,
    StudentCreateSerializer,
    StudentPaymentSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
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


class StudentPaymentUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = StudentPaymentSerializer


class StudentPaymentListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = StudentPaymentSerializer

    def get_queryset(self):
        queryset = Student.objects.all()
        payment_status = self.request.query_params.get("payment_status")

        if payment_status == "paid":
            queryset = queryset.filter(
                monthly_payment_cents__isnull=False, payment_day__isnull=False
            )
        elif payment_status == "not_paid":
            queryset = queryset.filter(
                monthly_payment_cents__isnull=True
            ) | queryset.filter(payment_day__isnull=True)

        return queryset.order_by("name")


class StudentPaymentBulkUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request):
        student_ids = request.data.get("student_ids", [])
        monthly_payment_cents = request.data.get("monthly_payment_cents")
        payment_day = request.data.get("payment_day")

        if not student_ids:
            return Response(
                {"error": "student_ids is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if monthly_payment_cents is None and payment_day is None:
            return Response(
                {
                    "error": "At least one field (monthly_payment_cents or payment_day) must be provided"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        update_data = {}
        if monthly_payment_cents is not None:
            if monthly_payment_cents < 0:
                return Response(
                    {"error": "Monthly payment cannot be negative"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            update_data["monthly_payment_cents"] = monthly_payment_cents

        if payment_day is not None:
            if payment_day < 1 or payment_day > 31:
                return Response(
                    {"error": "Payment day must be between 1 and 31"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            update_data["payment_day"] = payment_day

        updated_count = Student.objects.filter(id__in=student_ids).update(**update_data)

        return Response(
            {
                "message": f"Successfully updated {updated_count} students",
                "updated_count": updated_count,
                "updated_data": update_data,
            }
        )
