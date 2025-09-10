from rest_framework import serializers
from .models import Poll, Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "poll", "option"]
        read_only_fields = ["id"]


class PollSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ["id", "date", "status", "votes"]
        read_only_fields = ["id", "votes"]
