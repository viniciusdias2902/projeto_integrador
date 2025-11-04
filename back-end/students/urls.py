from django.urls import path
from . import views

urlpatterns = [
    path(
        "students/", views.StudentListCreateView.as_view(), name="students-create-list"
    ),
    path(
        "students/<int:pk>/",
        views.StudentRetrieveUpdateDestroyView.as_view(),
        name="students-retrieve-update-destroy",
    ),
    path(
        "students/<int:pk>/payment/",
        views.StudentPaymentUpdateView.as_view(),
        name="student-payment-update",
    ),
    path(
        "students/payments/",
        views.StudentPaymentListView.as_view(),
        name="student-payment-list",
    ),
    path(
        "students/payments/bulk-update/",
        views.StudentPaymentBulkUpdateView.as_view(),
        name="student-payment-bulk-update",
    ),
]
