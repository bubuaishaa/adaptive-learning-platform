from django.urls import path

from .views import CompleteLearningPathStepView, MyLearningPathView, MyRecommendationsView, RegenerateRecommendationsView

urlpatterns = [
    path("recommendations/my/", MyRecommendationsView.as_view(), name="my-recommendations"),
    path("recommendations/regenerate/", RegenerateRecommendationsView.as_view(), name="regenerate-recommendations"),
    path("learning-path/my/", MyLearningPathView.as_view(), name="my-learning-path"),
    path("learning-path/steps/<int:pk>/complete/", CompleteLearningPathStepView.as_view(), name="complete-learning-step"),
]
