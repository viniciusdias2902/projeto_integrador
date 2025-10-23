from django.urls import path
from . import views

urlpatterns = [
    path("trips/", views.TripListView.as_view(), name="trip-list"),
    path("trips/create/", views.TripCreateView.as_view(), name="trip-create"),
    path("trips/<int:pk>/", views.TripDetailView.as_view(), name="trip-detail"),
    path("trips/<int:pk>/start/", views.TripStartView.as_view(), name="trip-start"),
    path(
        "trips/<int:pk>/next_stop/",
        views.TripNextStopView.as_view(),
        name="trip-next-stop",
    ),
    path(
        "trips/<int:pk>/complete/",
        views.TripCompleteView.as_view(),
        name="trip-complete",
    ),
    path(
        "trips/<int:pk>/status/",
        views.TripCurrentStatusView.as_view(),
        name="trip-status",
    ),
]
