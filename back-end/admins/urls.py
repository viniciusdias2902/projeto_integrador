from django.urls import path
from . import views

urlpatterns = [
    path("admins/", views.AdminListCreateView.as_view(), name="admins-create-list"),
    path(
        "admins/<int:pk>/",
        views.AdminRetrieveUpdateDestroyView.as_view(),
        name="admins-retrieve-update-destroy",
    ),
]
