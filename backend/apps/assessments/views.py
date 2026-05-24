from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsStudent, IsTeacherOrAdmin

from .models import AnswerOption, Question, Test, TestAttempt
from .permissions import IsTeacherOwnerOrAdminOrReadOnly
from .serializers import AnswerOptionSerializer, QuestionSerializer, TestAttemptSerializer, TestSerializer, TestSubmitSerializer
from .services import submit_test


class TestListCreateView(generics.ListCreateAPIView):
    serializer_class = TestSerializer
    permission_classes = [IsTeacherOwnerOrAdminOrReadOnly]

    def get_queryset(self):
        queryset = Test.objects.select_related("course", "course__teacher", "topic").prefetch_related("questions__options", "questions__topic")
        if self.request.user.role == "admin":
            return queryset
        if self.request.user.role == "teacher":
            return queryset.filter(course__teacher=self.request.user)
        return queryset.filter(is_active=True, course__is_active=True)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsTeacherOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        course = serializer.validated_data["course"]
        if self.request.user.role != "admin" and course.teacher_id != self.request.user.id:
            raise PermissionDenied("Нельзя создавать тесты в чужом курсе.")
        serializer.save()


class TestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestSerializer
    permission_classes = [IsTeacherOwnerOrAdminOrReadOnly]

    def get_queryset(self):
        queryset = Test.objects.select_related("course", "course__teacher", "topic").prefetch_related("questions__options", "questions__topic")
        if self.request.user.role == "admin":
            return queryset
        if self.request.user.role == "teacher":
            return queryset.filter(course__teacher=self.request.user)
        return queryset.filter(is_active=True, course__is_active=True)


class QuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsTeacherOwnerOrAdminOrReadOnly]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsTeacherOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Question.objects.select_related("test", "test__course", "test__course__teacher", "topic").prefetch_related("options")
        if self.request.user.role == "admin":
            return queryset
        if self.request.user.role == "teacher":
            return queryset.filter(test__course__teacher=self.request.user)
        return queryset.filter(test__is_active=True, test__course__is_active=True)

    def perform_create(self, serializer):
        test = serializer.validated_data["test"]
        topic = serializer.validated_data["topic"]
        if topic.course_id != test.course_id:
            raise PermissionDenied("Тема вопроса должна относиться к курсу теста.")
        if self.request.user.role != "admin" and test.course.teacher_id != self.request.user.id:
            raise PermissionDenied("Нельзя создавать вопросы в чужом тесте.")
        serializer.save()


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsTeacherOwnerOrAdminOrReadOnly]

    def get_queryset(self):
        queryset = Question.objects.select_related("test", "test__course", "test__course__teacher", "topic").prefetch_related("options")
        if self.request.user.role == "admin":
            return queryset
        if self.request.user.role == "teacher":
            return queryset.filter(test__course__teacher=self.request.user)
        return queryset.filter(test__is_active=True, test__course__is_active=True)


class AnswerOptionListCreateView(generics.ListCreateAPIView):
    serializer_class = AnswerOptionSerializer
    permission_classes = [IsTeacherOwnerOrAdminOrReadOnly]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsTeacherOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = AnswerOption.objects.select_related("question", "question__test", "question__test__course", "question__test__course__teacher")
        if self.request.user.role == "admin":
            return queryset
        if self.request.user.role == "teacher":
            return queryset.filter(question__test__course__teacher=self.request.user)
        return queryset.filter(question__test__is_active=True, question__test__course__is_active=True)

    def perform_create(self, serializer):
        question = serializer.validated_data["question"]
        if self.request.user.role != "admin" and question.test.course.teacher_id != self.request.user.id:
            raise PermissionDenied("Нельзя создавать варианты ответа в чужом тесте.")
        serializer.save()


class AnswerOptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerOptionSerializer
    permission_classes = [IsTeacherOwnerOrAdminOrReadOnly]

    def get_queryset(self):
        queryset = AnswerOption.objects.select_related("question", "question__test", "question__test__course", "question__test__course__teacher")
        if self.request.user.role == "admin":
            return queryset
        if self.request.user.role == "teacher":
            return queryset.filter(question__test__course__teacher=self.request.user)
        return queryset.filter(question__test__is_active=True, question__test__course__is_active=True)


class SubmitTestView(APIView):
    permission_classes = [IsStudent]

    def post(self, request, pk):
        serializer = TestSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = submit_test(
            request.user,
            pk,
            serializer.validated_data["answers"],
            serializer.validated_data.get("started_at"),
        )
        return Response(result, status=status.HTTP_201_CREATED)


class AttemptListView(generics.ListAPIView):
    serializer_class = TestAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = TestAttempt.objects.select_related("student", "test").prefetch_related("answers__question", "answers__selected_option")
        if self.request.user.role == "student":
            return qs.filter(student=self.request.user)
        if self.request.user.role == "teacher":
            return qs.filter(test__course__teacher=self.request.user)
        return qs


class AttemptDetailView(generics.RetrieveAPIView):
    serializer_class = TestAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = TestAttempt.objects.select_related("student", "test").prefetch_related("answers__question", "answers__selected_option")
        if self.request.user.role == "student":
            return qs.filter(student=self.request.user)
        if self.request.user.role == "teacher":
            return qs.filter(test__course__teacher=self.request.user)
        return qs
