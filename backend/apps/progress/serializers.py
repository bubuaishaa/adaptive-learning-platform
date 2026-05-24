from rest_framework import serializers

from .models import StudentProgress, TopicProgress


class TopicProgressSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(source="topic.title", read_only=True)
    topic_id = serializers.IntegerField(source="topic.id", read_only=True)
    course = serializers.CharField(source="topic.course.title", read_only=True)

    class Meta:
        model = TopicProgress
        fields = ["id", "topic_id", "topic", "course", "mastery_percent", "level", "attempts_count", "last_score", "updated_at"]


class StudentProgressSerializer(serializers.ModelSerializer):
    student = serializers.CharField(source="student.username", read_only=True)

    class Meta:
        model = StudentProgress
        fields = ["id", "student", "overall_percent", "overall_level", "completed_tests", "updated_at"]
