from rest_framework import serializers

from .models import Course, Lesson, Topic


class LessonSerializer(serializers.ModelSerializer):
    topic_title = serializers.CharField(source="topic.title", read_only=True)
    course_id = serializers.IntegerField(source="topic.course_id", read_only=True)

    class Meta:
        model = Lesson
        fields = ["id", "topic", "topic_title", "course_id", "title", "content", "video_url", "lesson_type", "order", "created_at"]


class TopicSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ["id", "course", "title", "description", "order", "lessons"]


class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source="teacher.get_full_name", read_only=True)
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "description", "teacher", "teacher_name", "image", "is_active", "created_at", "updated_at", "topics"]
        read_only_fields = ["teacher", "created_at", "updated_at"]
