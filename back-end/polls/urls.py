from django.urls import path
from .views import (
    PollListView,
    PollDetailView,
    PollBoardingListView,
    CreateWeeklyPollsView,
    CleanOldPollsView,
    VoteCreateView,
    VoteListView,
    VoteUpdateView,
)

urlpatterns = [
    path("polls/", PollListView.as_view(), name="poll-list"),
    path("polls/<int:pk>/", PollDetailView.as_view(), name="poll-detail"),
    path(
        "polls/<int:pk>/boarding_list/",
        PollBoardingListView.as_view(),
        name="poll-boarding-list",
    ),
    path(
        "polls/create_weekly/",
        CreateWeeklyPollsView.as_view(),
        name="create-weekly-polls",
    ),
    path(
        "polls/clean_old/",
        CleanOldPollsView.as_view(),
        name="clean-old-polls",
    ),
    path("votes/", VoteListView.as_view(), name="vote-list"),
    path("votes/create/", VoteCreateView.as_view(), name="vote-create"),
    path("votes/<int:pk>/update/", VoteUpdateView.as_view(), name="vote-update"),
]
