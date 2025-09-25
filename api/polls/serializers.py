from rest_framework import serializers
from .models import Poll, Vote
from students.models import Student
from common.serializer import BoardingPointSerializer 


class StudentNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name"]


class VoteSerializer(serializers.ModelSerializer):
    student = StudentNestedSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = ["id", "poll", "option", "student"]
        read_only_fields = ["id", "student"]


class PollSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ["id", "date", "status", "votes"]
        read_only_fields = ["id", "votes"]

class BoardingListStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name']

class BoardingListSerializer(serializers.Serializer):
    point = BoardingPointSerializer(source='boarding_list')
    students = BoardingListStudentSerializer(many=True)