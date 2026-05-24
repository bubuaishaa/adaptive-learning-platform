from django.urls import path

from .views import (
    AnswerOptionListCreateView,
    AnswerOptionDetailView,
    AttemptDetailView,
    AttemptListView,
    QuestionDetailView,
    QuestionListCreateView,
    SubmitTestView,
    TestDetailView,
    TestListCreateView,
)

urlpatterns = [
    path("tests/", TestListCreateView.as_view(), name="tests"),
    path("tests/<int:pk>/", TestDetailView.as_view(), name="test-detail"),
    path("tests/<int:pk>/submit/", SubmitTestView.as_view(), name="test-submit"),
    path("questions/", QuestionListCreateView.as_view(), name="questions"),
    path("questions/<int:pk>/", QuestionDetailView.as_view(), name="question-detail"),
    path("answer-options/", AnswerOptionListCreateView.as_view(), name="answer-options"),
    path("answer-options/<int:pk>/", AnswerOptionDetailView.as_view(), name="answer-option-detail"),
    path("attempts/", AttemptListView.as_view(), name="attempts"),
    path("attempts/<int:pk>/", AttemptDetailView.as_view(), name="attempt-detail"),
]
