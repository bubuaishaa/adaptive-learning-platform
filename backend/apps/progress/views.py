from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User
from apps.users.permissions import IsTeacherOrAdmin

from .models import StudentProgress, TopicProgress
from .serializers import StudentProgressSerializer, TopicProgressSerializer
from .services import update_student_progress


class MyProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.Role.STUDENT:
            return Response({"detail": "Этот endpoint доступен только студенту."}, status=403)
        summary = update_student_progress(request.user)
        topics = TopicProgress.objects.filter(student=request.user).select_related("topic", "topic__course")
        return Response({
            "summary": StudentProgressSerializer(summary).data,
            "topics": TopicProgressSerializer(topics, many=True).data,
        })


class TopicProgressListView(generics.ListAPIView):
    serializer_class = TopicProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != User.Role.STUDENT:
            return TopicProgress.objects.none()
        return TopicProgress.objects.filter(student=self.request.user).select_related("topic", "topic__course")


class ProgressSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.Role.STUDENT:
            return Response({"detail": "Этот endpoint доступен только студенту."}, status=403)
        return Response(StudentProgressSerializer(update_student_progress(request.user)).data)


class StudentProgressDetailView(APIView):
    permission_classes = [IsTeacherOrAdmin]

    def get(self, request, pk):
        student = get_object_or_404(User, pk=pk, role=User.Role.STUDENT)
        if request.user.role == User.Role.TEACHER:
            has_related_attempts = student.test_attempts.filter(test__course__teacher=request.user).exists()
            if not has_related_attempts:
                return Response({"detail": "Нет доступа к прогрессу этого студента."}, status=403)
        summary = update_student_progress(student)
        topics = TopicProgress.objects.filter(student=student).select_related("topic", "topic__course")
        if request.user.role == User.Role.TEACHER:
            topics = topics.filter(topic__course__teacher=request.user)
        return Response({
            "summary": StudentProgressSerializer(summary).data,
            "topics": TopicProgressSerializer(topics, many=True).data,
        })
