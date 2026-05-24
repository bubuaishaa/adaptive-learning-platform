from apps.courses.models import Lesson, Topic
from apps.progress.models import TopicProgress

from .models import LearningPath, LearningPathStep, Recommendation


LEVEL_TO_LESSON_TYPE = {
    TopicProgress.Level.LOW: Lesson.LessonType.BEGINNER,
    TopicProgress.Level.MEDIUM: Lesson.LessonType.REINFORCEMENT,
    TopicProgress.Level.HIGH: Lesson.LessonType.ADVANCED,
}

LEVEL_PRIORITY = {
    TopicProgress.Level.LOW: 1,
    TopicProgress.Level.MEDIUM: 2,
    TopicProgress.Level.HIGH: 3,
}


def build_reason(topic_progress, lesson_type):
    if topic_progress.level == TopicProgress.Level.LOW:
        return f"Показатель по теме {topic_progress.topic.title} составляет {topic_progress.mastery_percent}%, поэтому рекомендован базовый материал для повторного изучения."
    if topic_progress.level == TopicProgress.Level.MEDIUM:
        return f"Показатель по теме {topic_progress.topic.title} составляет {topic_progress.mastery_percent}%, поэтому рекомендованы закрепляющие задания."
    return f"Показатель по теме {topic_progress.topic.title} составляет {topic_progress.mastery_percent}%, поэтому рекомендован материал повышенной сложности."


def _advanced_lessons_for(topic):
    lessons = list(topic.lessons.filter(lesson_type=Lesson.LessonType.ADVANCED))
    next_topic = Topic.objects.filter(course=topic.course, order__gt=topic.order).order_by("order").first()
    if next_topic:
        lessons.extend(next_topic.lessons.filter(lesson_type=Lesson.LessonType.BEGINNER))
    return lessons


def generate_recommendations(student):
    topic_progress_items = sorted(
        TopicProgress.objects.filter(student=student)
        .select_related("topic", "topic__course")
        .prefetch_related("topic__lessons"),
        key=lambda item: (LEVEL_PRIORITY[item.level], item.mastery_percent, item.topic.course_id, item.topic.order),
    )
    learning_path, _ = LearningPath.objects.get_or_create(student=student, title="Жеке окуу траекториясы")
    created_recommendations = []
    current_recommendation_ids = []
    current_step_ids = []
    order = 1

    for topic_progress in topic_progress_items:
        lesson_type = LEVEL_TO_LESSON_TYPE[topic_progress.level]
        lessons = _advanced_lessons_for(topic_progress.topic) if topic_progress.level == TopicProgress.Level.HIGH else topic_progress.topic.lessons.filter(lesson_type=lesson_type)
        reason = build_reason(topic_progress, lesson_type)

        for lesson in lessons:
            previous = Recommendation.objects.filter(student=student, topic=topic_progress.topic, lesson=lesson).first()
            recommendation, _ = Recommendation.objects.update_or_create(
                student=student,
                topic=topic_progress.topic,
                lesson=lesson,
                defaults={
                    "reason": reason,
                    "level": topic_progress.level,
                    "is_completed": previous.is_completed if previous else False,
                },
            )
            step, _ = LearningPathStep.objects.update_or_create(
                learning_path=learning_path,
                lesson=lesson,
                defaults={"topic": topic_progress.topic, "order": order},
            )
            created_recommendations.append(recommendation)
            current_recommendation_ids.append(recommendation.id)
            current_step_ids.append(step.id)
            order += 1

    Recommendation.objects.filter(student=student).exclude(id__in=current_recommendation_ids).delete()
    LearningPathStep.objects.filter(learning_path=learning_path).exclude(id__in=current_step_ids).delete()
    return created_recommendations
