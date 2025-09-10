from django.urls import path
from .views import (
    PollListView,
    PollDetailView,
    PollBoardingListView,
    VoteCreateView,
    VoteListView,
    CreateTestPollsView,
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
        "polls/create_test_polls/",
        CreateTestPollsView.as_view(),
        name="create-test-polls",
    ),
    path("votes/", VoteListView.as_view(), name="vote-list"),
    path("votes/create/", VoteCreateView.as_view(), name="vote-create"),
]
