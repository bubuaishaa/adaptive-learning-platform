from rest_framework import serializers

from .models import AnswerOption, Question, StudentAnswer, Test, TestAttempt


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ["id", "question", "text", "is_correct"]
        extra_kwargs = {"is_correct": {"write_only": True}}


class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True, read_only=True)
    topic_title = serializers.CharField(source="topic.title", read_only=True)

    class Meta:
        model = Question
        fields = ["id", "test", "topic", "topic_title", "text", "difficulty", "options"]


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    course_title = serializers.CharField(source="course.title", read_only=True)
    topic_title = serializers.CharField(source="topic.title", read_only=True)

    class Meta:
        model = Test
        fields = ["id", "course", "course_title", "topic", "topic_title", "title", "description", "time_limit", "is_active", "created_at", "questions"]


class StudentAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source="question.text", read_only=True)
    selected_text = serializers.CharField(source="selected_option.text", read_only=True)

    class Meta:
        model = StudentAnswer
        fields = ["id", "question", "question_text", "selected_option", "selected_text", "is_correct"]


class TestAttemptSerializer(serializers.ModelSerializer):
    test_title = serializers.CharField(source="test.title", read_only=True)
    answers = StudentAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = TestAttempt
        fields = ["id", "student", "test", "test_title", "score", "started_at", "completed_at", "is_completed", "answers"]
        read_only_fields = ["student", "score", "started_at", "completed_at", "is_completed"]


class SubmitAnswerSerializer(serializers.Serializer):
    question = serializers.IntegerField()
    selected_option = serializers.IntegerField()


class TestSubmitSerializer(serializers.Serializer):
    answers = SubmitAnswerSerializer(many=True)
    started_at = serializers.DateTimeField(required=False)
