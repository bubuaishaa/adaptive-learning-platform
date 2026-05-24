from django.db.models import Avg

from apps.assessments.models import StudentAnswer, TestAttempt
from apps.courses.models import Topic

from .models import StudentProgress, TopicProgress


def get_level(mastery_percent):
    if mastery_percent < 50:
        return TopicProgress.Level.LOW
    if mastery_percent < 75:
        return TopicProgress.Level.MEDIUM
    return TopicProgress.Level.HIGH


def calculate_topic_mastery(student, topic):
    progress = TopicProgress.objects.filter(student=student, topic=topic).first()
    return progress.mastery_percent if progress else 0


def _topic_attempt_scores(student, topic):
    attempts = (
        TestAttempt.objects.filter(student=student, is_completed=True, answers__question__topic=topic)
        .distinct()
        .order_by("completed_at", "id")
    )
    scores = []
    for attempt in attempts:
        answers = StudentAnswer.objects.filter(attempt=attempt, question__topic=topic)
        total = answers.count()
        correct = answers.filter(is_correct=True).count()
        if total:
            scores.append(round((correct / total) * 100, 2))
    return scores


def _weighted_recent_average(scores, window=3):
    """
    Mastery is a weighted average of the last topic-level attempts.

    Diploma explanation: the platform does not let one accidental result fully
    overwrite progress. Recent attempts matter more, but previous attempts still
    stabilize the estimate. For the last three scores weights are 1, 2, 3.
    Example: scores 40, 60, 80 -> (40*1 + 60*2 + 80*3) / 6 = 66.67.
    """
    recent_scores = scores[-window:]
    if not recent_scores:
        return 0
    weights = range(1, len(recent_scores) + 1)
    weighted_sum = sum(score * weight for score, weight in zip(recent_scores, weights))
    return round(weighted_sum / sum(weights), 2)


def update_topic_progress(student, topic, correct, total, recalculate_overall=True):
    current_score = round((correct / total) * 100, 2) if total else 0
    historical_scores = _topic_attempt_scores(student, topic)
    mastery_percent = _weighted_recent_average(historical_scores) if historical_scores else current_score
    level = get_level(mastery_percent)
    progress, _ = TopicProgress.objects.get_or_create(student=student, topic=topic)
    progress.mastery_percent = mastery_percent
    progress.level = level
    progress.last_score = current_score
    progress.attempts_count = len(historical_scores) or progress.attempts_count + 1
    progress.save(update_fields=["mastery_percent", "level", "last_score", "attempts_count", "updated_at"])
    if recalculate_overall:
        update_student_progress(student)
    return progress


def update_student_progress(student):
    course_ids = TestAttempt.objects.filter(student=student, is_completed=True).values_list("test__course_id", flat=True).distinct()
    topic_ids = list(Topic.objects.filter(course_id__in=course_ids).values_list("id", flat=True))

    for topic in Topic.objects.filter(id__in=topic_ids):
        TopicProgress.objects.get_or_create(
            student=student,
            topic=topic,
            defaults={"mastery_percent": 0, "level": TopicProgress.Level.LOW, "last_score": 0},
        )

    progress_queryset = TopicProgress.objects.filter(student=student)
    if topic_ids:
        progress_queryset = progress_queryset.filter(topic_id__in=topic_ids)

    aggregate = progress_queryset.aggregate(avg=Avg("mastery_percent"))
    overall_percent = round(aggregate["avg"] or 0, 2)
    completed_tests = TestAttempt.objects.filter(student=student, is_completed=True).count()
    progress, _ = StudentProgress.objects.get_or_create(student=student)
    progress.overall_percent = overall_percent
    progress.overall_level = get_level(overall_percent)
    progress.completed_tests = completed_tests
    progress.save(update_fields=["overall_percent", "overall_level", "completed_tests", "updated_at"])
    return progress
