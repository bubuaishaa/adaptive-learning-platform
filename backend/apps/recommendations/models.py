from django.conf import settings
from django.db import models

from apps.courses.models import Lesson, Topic


class Recommendation(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recommendations")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="recommendations")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="recommendations")
    reason = models.TextField()
    level = models.CharField(max_length=20)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "topic", "lesson")
        ordering = ["topic__order", "lesson__order"]

    def __str__(self):
        return f"{self.student} - {self.lesson}"


class LearningPath(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="learning_paths")
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class LearningPathStep(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Күтүүдө"
        IN_PROGRESS = "in_progress", "Аткарылууда"
        COMPLETED = "completed", "Аякталды"

    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name="steps")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="learning_path_steps")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="learning_path_steps")
    order = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        unique_together = ("learning_path", "lesson")
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.learning_path} - {self.lesson}"
