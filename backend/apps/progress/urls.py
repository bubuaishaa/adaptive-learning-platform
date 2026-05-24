from django.urls import path

from .views import MyProgressView, ProgressSummaryView, StudentProgressDetailView, TopicProgressListView

urlpatterns = [
    path("my/", MyProgressView.as_view(), name="my-progress"),
    path("topics/", TopicProgressListView.as_view(), name="topic-progress"),
    path("summary/", ProgressSummaryView.as_view(), name="progress-summary"),
    path("student/<int:pk>/", StudentProgressDetailView.as_view(), name="student-progress"),
]
