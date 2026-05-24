from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsTeacherOwnerOrAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_authenticated and request.user.role in ["teacher", "admin"])

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        if request.user.role == "admin":
            return True

        course = getattr(obj, "course", None)
        if hasattr(obj, "test"):
            course = obj.test.course
        if hasattr(obj, "question"):
            course = obj.question.test.course
        return bool(request.user.role == "teacher" and course and course.teacher_id == request.user.id)
