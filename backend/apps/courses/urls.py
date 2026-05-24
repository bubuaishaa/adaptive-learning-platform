from django.urls import path

from .views import (
    CourseDetailView,
    CourseListCreateView,
    CourseTopicsView,
    LessonDetailView,
    LessonListCreateView,
    TopicDetailView,
    TopicLessonsView,
    TopicListCreateView,
)

urlpatterns = [
    path("courses/", CourseListCreateView.as_view(), name="courses"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course-detail"),
    path("courses/<int:pk>/topics/", CourseTopicsView.as_view(), name="course-topics"),
    path("topics/", TopicListCreateView.as_view(), name="topics"),
    path("topics/<int:pk>/", TopicDetailView.as_view(), name="topic-detail"),
    path("topics/<int:pk>/lessons/", TopicLessonsView.as_view(), name="topic-lessons"),
    path("lessons/", LessonListCreateView.as_view(), name="lessons"),
    path("lessons/<int:pk>/", LessonDetailView.as_view(), name="lesson-detail"),
]
