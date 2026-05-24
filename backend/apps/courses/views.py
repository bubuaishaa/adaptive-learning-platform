from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from .models import Course, Lesson, Topic
from .permissions import IsTeacherOrAdminOrReadOnly
from .serializers import CourseSerializer, LessonSerializer, TopicSerializer


class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrAdminOrReadOnly]

    def get_queryset(self):
        queryset = Course.objects.select_related("teacher").prefetch_related("topics__lessons").order_by("-created_at")
        if self.request.user.role == "admin":
            return queryset
        if self.request.user.role == "teacher":
            return queryset.filter(teacher=self.request.user)
        return queryset.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrAdminOrReadOnly]
    def get_queryset(self):
        queryset = Course.objects.select_related("teacher").prefetch_related("topics__lessons")
        if self.request.user.role == "admin":
            return queryset
        if self.request.user.role == "teacher":
            return queryset.filter(teacher=self.request.user)
        return queryset.filter(is_active=True)


class TopicListCreateView(generics.ListCreateAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsTeacherOrAdminOrReadOnly]
    def get_queryset(self):
        queryset = Topic.objects.select_related("course", "course__teacher").prefetch_related("lessons")
        if self.request.user.role == "admin":
            return queryset
        if self.request.user.role == "teacher":
            return queryset.filter(course__teacher=self.request.user)
        return queryset.filter(course__is_active=True)

    def perform_create(self, serializer):
        course = serializer.validated_data["course"]
        if self.request.user.role != "admin" and course.teacher_id != self.request.user.id:
            raise PermissionDenied("Нельзя создавать темы в чужом курсе.")
        serializer.save()


class TopicDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsTeacherOrAdminOrReadOnly]

    def get_queryset(self):
        queryset = Topic.objects.select_related("course", "course__teacher").prefetch_related("lessons")
        if self.request.user.role == "admin":
            return queryset
        if self.request.user.role == "teacher":
            return queryset.filter(course__teacher=self.request.user)
        return queryset.filter(course__is_active=True)


class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsTeacherOrAdminOrReadOnly]
    def get_queryset(self):
        queryset = Lesson.objects.select_related("topic", "topic__course", "topic__course__teacher")
        if self.request.user.role == "admin":
            return queryset
        if self.request.user.role == "teacher":
            return queryset.filter(topic__course__teacher=self.request.user)
        return queryset.filter(topic__course__is_active=True)

    def perform_create(self, serializer):
        topic = serializer.validated_data["topic"]
        if self.request.user.role != "admin" and topic.course.teacher_id != self.request.user.id:
            raise PermissionDenied("Нельзя создавать уроки в чужом курсе.")
        serializer.save()


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsTeacherOrAdminOrReadOnly]
    def get_queryset(self):
        queryset = Lesson.objects.select_related("topic", "topic__course", "topic__course__teacher")
        if self.request.user.role == "admin":
            return queryset
        if self.request.user.role == "teacher":
            return queryset.filter(topic__course__teacher=self.request.user)
        return queryset.filter(topic__course__is_active=True)


class CourseTopicsView(generics.ListAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsTeacherOrAdminOrReadOnly]

    def get_queryset(self):
        queryset = Topic.objects.filter(course_id=self.kwargs["pk"]).select_related("course", "course__teacher").prefetch_related("lessons")
        if self.request.user.role == "admin":
            return queryset
        if self.request.user.role == "teacher":
            return queryset.filter(course__teacher=self.request.user)
        return queryset.filter(course__is_active=True)


class TopicLessonsView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsTeacherOrAdminOrReadOnly]

    def get_queryset(self):
        queryset = Lesson.objects.filter(topic_id=self.kwargs["pk"]).select_related("topic", "topic__course", "topic__course__teacher")
        if self.request.user.role == "admin":
            return queryset
        if self.request.user.role == "teacher":
            return queryset.filter(topic__course__teacher=self.request.user)
        return queryset.filter(topic__course__is_active=True)
