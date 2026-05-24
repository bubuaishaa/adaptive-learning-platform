from rest_framework import serializers

from .models import LearningPath, LearningPathStep, Recommendation


class RecommendationSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(source="topic.title", read_only=True)
    topic_id = serializers.IntegerField(source="topic.id", read_only=True)
    lesson = serializers.CharField(source="lesson.title", read_only=True)
    lesson_id = serializers.IntegerField(source="lesson.id", read_only=True)
    lesson_type = serializers.CharField(source="lesson.lesson_type", read_only=True)

    class Meta:
        model = Recommendation
        fields = ["id", "topic_id", "topic", "lesson_id", "lesson", "reason", "level", "lesson_type", "is_completed", "created_at"]


class LearningPathStepSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(source="topic.title", read_only=True)
    lesson = serializers.CharField(source="lesson.title", read_only=True)
    lesson_id = serializers.IntegerField(source="lesson.id", read_only=True)
    lesson_type = serializers.CharField(source="lesson.lesson_type", read_only=True)

    class Meta:
        model = LearningPathStep
        fields = ["id", "topic", "lesson", "lesson_id", "lesson_type", "order", "status"]


class LearningPathSerializer(serializers.ModelSerializer):
    steps = LearningPathStepSerializer(many=True, read_only=True)

    class Meta:
        model = LearningPath
        fields = ["id", "title", "created_at", "updated_at", "steps"]
