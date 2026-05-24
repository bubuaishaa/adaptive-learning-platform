from django.conf import settings
from django.db import models

from apps.courses.models import Topic


class TopicProgress(models.Model):
    class Level(models.TextChoices):
        LOW = "low", "Төмөн"
        MEDIUM = "medium", "Орточо"
        HIGH = "high", "Жогорку"

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="topic_progress")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="student_progress")
    mastery_percent = models.FloatField(default=0)
    level = models.CharField(max_length=20, choices=Level.choices, default=Level.LOW)
    attempts_count = models.PositiveIntegerField(default=0)
    last_score = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "topic")
        ordering = ["topic__course_id", "topic__order"]

    def __str__(self):
        return f"{self.student} - {self.topic}: {self.mastery_percent}%"


class StudentProgress(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="overall_progress")
    overall_percent = models.FloatField(default=0)
    overall_level = models.CharField(max_length=20, choices=TopicProgress.Level.choices, default=TopicProgress.Level.LOW)
    completed_tests = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.overall_percent}%"
