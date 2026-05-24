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
            name="LearningPath",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="learning_paths", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Recommendation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reason", models.TextField()),
                ("level", models.CharField(max_length=20)),
                ("is_completed", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("lesson", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="recommendations", to="courses.lesson")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="recommendations", to=settings.AUTH_USER_MODEL)),
                ("topic", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="recommendations", to="courses.topic")),
            ],
            options={"ordering": ["topic__order", "lesson__order"], "unique_together": {("student", "topic", "lesson")}},
        ),
        migrations.CreateModel(
            name="LearningPathStep",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=1)),
                ("status", models.CharField(choices=[("pending", "Күтүүдө"), ("in_progress", "Аткарылууда"), ("completed", "Аякталды")], default="pending", max_length=20)),
                ("learning_path", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="steps", to="recommendations.learningpath")),
                ("lesson", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="learning_path_steps", to="courses.lesson")),
                ("topic", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="learning_path_steps", to="courses.topic")),
            ],
            options={"ordering": ["order", "id"], "unique_together": {("learning_path", "lesson")}},
        ),
    ]
