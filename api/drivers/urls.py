from django.urls import path
from . import views

urlpatterns = [
    path("drivers/", views.DriverListCreateView.as_view(), name="drivers-create-list"),
    path(
        "drivers/<int:pk>/",
        views.DriverRetrieveUpdateDestroyView.as_view(),
        name="drivers-retrieve-update-destroy",
    ),
]
