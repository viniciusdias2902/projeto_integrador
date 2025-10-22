from rest_framework import serializers
from .models import Poll, Vote
from students.models import Student
from boarding_points.serializers import BoardingPointSerializer 


class StudentNestedSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    
    class Meta:
        model = Student
        fields = ["id", "name", "user_id"]


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
    point = BoardingPointSerializer(source='boarding_point')
    students = BoardingListStudentSerializer(many=True)