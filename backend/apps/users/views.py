from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .permissions import IsAdmin, IsTeacherOrAdmin
from .serializers import AdminUserUpdateSerializer, LoginSerializer, RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.all().order_by("id")


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = AdminUserUpdateSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.all().order_by("id")


class StudentListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsTeacherOrAdmin]

    def get_queryset(self):
        if self.request.user.role == User.Role.TEACHER:
            return User.objects.filter(
                role=User.Role.STUDENT,
                test_attempts__test__course__teacher=self.request.user,
            ).distinct().order_by("id")
        return User.objects.filter(role=User.Role.STUDENT).order_by("id")


class TeacherListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return User.objects.filter(role=User.Role.TEACHER).order_by("id")
