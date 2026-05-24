from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsStudent

from .models import LearningPath, LearningPathStep, Recommendation
from .serializers import LearningPathSerializer, RecommendationSerializer
from .services import generate_recommendations


class MyRecommendationsView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        generate_recommendations(request.user)
        queryset = Recommendation.objects.filter(student=request.user).select_related("topic", "lesson")
        return Response(RecommendationSerializer(queryset, many=True).data)


class RegenerateRecommendationsView(APIView):
    permission_classes = [IsStudent]

    def post(self, request):
        recommendations = generate_recommendations(request.user)
        return Response(RecommendationSerializer(recommendations, many=True).data)


class MyLearningPathView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        generate_recommendations(request.user)
        learning_path = LearningPath.objects.filter(student=request.user).prefetch_related("steps__topic", "steps__lesson").first()
        if not learning_path:
            learning_path = LearningPath.objects.create(student=request.user, title="Жеке окуу траекториясы")
        return Response(LearningPathSerializer(learning_path).data)


class CompleteLearningPathStepView(APIView):
    permission_classes = [IsStudent]

    def post(self, request, pk):
        step = get_object_or_404(LearningPathStep, pk=pk, learning_path__student=request.user)
        step.status = LearningPathStep.Status.COMPLETED
        step.save(update_fields=["status"])
        Recommendation.objects.filter(student=request.user, lesson=step.lesson).update(is_completed=True)
        return Response(LearningPathSerializer(step.learning_path).data)
