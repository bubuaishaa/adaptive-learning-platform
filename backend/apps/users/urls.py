from django.urls import path

from .views import StudentListView, TeacherListView, UserDetailView, UserListView

urlpatterns = [
    path("", UserListView.as_view(), name="users"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("students/", StudentListView.as_view(), name="students"),
    path("teachers/", TeacherListView.as_view(), name="teachers"),
]
