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
]
