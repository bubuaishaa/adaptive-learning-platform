from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.courses.models import Course, Lesson, Topic
from apps.progress.models import StudentProgress, TopicProgress
from apps.recommendations.models import LearningPathStep, Recommendation
from apps.users.models import User

from .models import AnswerOption, Question, Test, TestAttempt


class AdaptivePlatformAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.local",
            password="admin12345",
            role=User.Role.ADMIN,
        )
        self.teacher = User.objects.create_user(
            username="teacher",
            email="teacher@test.local",
            password="teacher12345",
            role=User.Role.TEACHER,
        )
        self.other_teacher = User.objects.create_user(
            username="other_teacher",
            email="other@test.local",
            password="teacher12345",
            role=User.Role.TEACHER,
        )
        self.student = User.objects.create_user(
            username="student",
            email="student@test.local",
            password="student12345",
            role=User.Role.STUDENT,
        )
        self.other_student = User.objects.create_user(
            username="other_student",
            email="otherstudent@test.local",
            password="student12345",
            role=User.Role.STUDENT,
        )

        self.course = Course.objects.create(title="Math", description="Math course", teacher=self.teacher)
        self.other_course = Course.objects.create(title="Physics", description="Other course", teacher=self.other_teacher)
        self.topic = Topic.objects.create(course=self.course, title="Fractions", order=1)
        self.second_topic = Topic.objects.create(course=self.course, title="Percents", order=2)
        self.other_topic = Topic.objects.create(course=self.other_course, title="Mechanics", order=1)

        for topic in [self.topic, self.second_topic]:
            Lesson.objects.create(topic=topic, title=f"{topic.title} beginner", content="Basic", lesson_type=Lesson.LessonType.BEGINNER)
            Lesson.objects.create(topic=topic, title=f"{topic.title} reinforcement", content="Practice", lesson_type=Lesson.LessonType.REINFORCEMENT)
            Lesson.objects.create(topic=topic, title=f"{topic.title} advanced", content="Advanced", lesson_type=Lesson.LessonType.ADVANCED)

        self.test = Test.objects.create(course=self.course, title="Diagnostic", time_limit=30)
        self.questions = [
            self._question(self.topic, "Q1", "A"),
            self._question(self.topic, "Q2", "A"),
            self._question(self.second_topic, "Q3", "A"),
        ]
        self.other_test = Test.objects.create(course=self.other_course, title="Other", time_limit=30)
        self.other_question = self._question(self.other_topic, "Other Q", "A", test=self.other_test)

    def _question(self, topic, text, correct_text, test=None):
        question = Question.objects.create(test=test or self.test, topic=topic, text=text)
        question.correct = AnswerOption.objects.create(question=question, text=correct_text, is_correct=True)
        question.wrong = AnswerOption.objects.create(question=question, text="Wrong", is_correct=False)
        return question

    def _answers(self, correctness):
        return [
            {
                "question": question.id,
                "selected_option": (question.correct if is_correct else question.wrong).id,
            }
            for question, is_correct in zip(self.questions, correctness)
        ]

    def _submit(self, correctness, user=None):
        self.client.force_authenticate(user=user or self.student)
        return self.client.post(
            f"/api/tests/{self.test.id}/submit/",
            {"answers": self._answers(correctness)},
            format="json",
        )

    def test_register_and_login(self):
        register_response = self.client.post(
            "/api/auth/register/",
            {
                "username": "new_student",
                "email": "new@test.local",
                "password": "student12345",
                "first_name": "New",
                "last_name": "Student",
                "role": "admin",
            },
            format="json",
        )
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(username="new_student").role, User.Role.STUDENT)

        login_response = self.client.post(
            "/api/auth/login/",
            {"username": "new_student", "password": "student12345"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)

    def test_role_permissions_limit_teacher_to_own_data(self):
        self.client.force_authenticate(user=self.other_teacher)
        course_response = self.client.patch(f"/api/courses/{self.course.id}/", {"title": "Hacked"}, format="json")
        test_response = self.client.patch(f"/api/tests/{self.test.id}/", {"title": "Hacked"}, format="json")
        self.assertEqual(course_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(test_response.status_code, status.HTTP_404_NOT_FOUND)

        self._submit([True, False, False], self.student)
        TestAttempt.objects.create(student=self.other_student, test=self.other_test, score=100, is_completed=True, completed_at=timezone.now())

        self.client.force_authenticate(user=self.teacher)
        attempts_response = self.client.get("/api/attempts/")
        self.assertEqual(attempts_response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(item["test"] == self.test.id for item in attempts_response.data))

    def test_submit_test_updates_progress_and_recommendations(self):
        response = self._submit([True, False, True])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["score"], 66.67)
        self.assertEqual(len(response.data["topic_results"]), 2)

        topic_progress = TopicProgress.objects.get(student=self.student, topic=self.topic)
        self.assertEqual(topic_progress.mastery_percent, 50)
        self.assertEqual(topic_progress.level, TopicProgress.Level.MEDIUM)

        overall = StudentProgress.objects.get(student=self.student)
        self.assertGreater(overall.overall_percent, 0)
        self.assertTrue(Recommendation.objects.filter(student=self.student).exists())
        self.assertTrue(LearningPathStep.objects.filter(learning_path__student=self.student).exists())

    def test_weighted_recent_mastery_uses_history(self):
        self._submit([False, False, True])
        self._submit([True, True, True])
        topic_progress = TopicProgress.objects.get(student=self.student, topic=self.topic)
        self.assertEqual(topic_progress.mastery_percent, 66.67)
        self.assertEqual(topic_progress.last_score, 100)

    def test_submit_rejects_edge_cases(self):
        self.client.force_authenticate(user=self.student)

        incomplete = self.client.post(
            f"/api/tests/{self.test.id}/submit/",
            {"answers": self._answers([True, False])},
            format="json",
        )
        self.assertEqual(incomplete.status_code, status.HTTP_400_BAD_REQUEST)

        duplicate = self.client.post(
            f"/api/tests/{self.test.id}/submit/",
            {"answers": [self._answers([True, False, True])[0], self._answers([False, False, True])[0], self._answers([True, False, True])[2]]},
            format="json",
        )
        self.assertEqual(duplicate.status_code, status.HTTP_400_BAD_REQUEST)

        foreign_question = self.client.post(
            f"/api/tests/{self.test.id}/submit/",
            {"answers": self._answers([True, False, True])[:-1] + [{"question": self.other_question.id, "selected_option": self.other_question.correct.id}]},
            format="json",
        )
        self.assertEqual(foreign_question.status_code, status.HTTP_400_BAD_REQUEST)

        foreign_option = self.client.post(
            f"/api/tests/{self.test.id}/submit/",
            {"answers": self._answers([True, False, True])[:-1] + [{"question": self.questions[-1].id, "selected_option": self.other_question.correct.id}]},
            format="json",
        )
        self.assertEqual(foreign_option.status_code, status.HTTP_400_BAD_REQUEST)

        expired = self.client.post(
            f"/api/tests/{self.test.id}/submit/",
            {"started_at": (timezone.now() - timedelta(hours=2)).isoformat(), "answers": self._answers([True, False, True])},
            format="json",
        )
        self.assertEqual(expired.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_test_is_rejected(self):
        empty_test = Test.objects.create(course=self.course, title="Empty")
        self.client.force_authenticate(user=self.student)
        response = self.client.post(f"/api/tests/{empty_test.id}/submit/", {"answers": []}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
