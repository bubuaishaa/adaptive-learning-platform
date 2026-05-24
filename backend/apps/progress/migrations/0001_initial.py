from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("courses", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="StudentProgress",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("overall_percent", models.FloatField(default=0)),
                ("overall_level", models.CharField(choices=[("low", "Төмөн"), ("medium", "Орточо"), ("high", "Жогорку")], default="low", max_length=20)),
                ("completed_tests", models.PositiveIntegerField(default=0)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("student", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="overall_progress", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="TopicProgress",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("mastery_percent", models.FloatField(default=0)),
                ("level", models.CharField(choices=[("low", "Төмөн"), ("medium", "Орточо"), ("high", "Жогорку")], default="low", max_length=20)),
                ("attempts_count", models.PositiveIntegerField(default=0)),
                ("last_score", models.FloatField(default=0)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="topic_progress", to=settings.AUTH_USER_MODEL)),
                ("topic", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="student_progress", to="courses.topic")),
            ],
            options={"ordering": ["topic__course_id", "topic__order"], "unique_together": {("student", "topic")}},
        ),
    ]
