from collections import defaultdict

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.progress.serializers import TopicProgressSerializer
from apps.progress.services import update_topic_progress, update_student_progress
from apps.recommendations.serializers import RecommendationSerializer
from apps.recommendations.services import generate_recommendations

from .models import StudentAnswer, Test, TestAttempt


@transaction.atomic
def submit_test(student, test_id, answers, started_at=None):
    test = get_object_or_404(Test.objects.prefetch_related("questions__options", "questions__topic"), pk=test_id, is_active=True)
    questions = list(test.questions.all())
    if not questions:
        raise ValidationError({"test": "Тест не содержит вопросов."})

    if started_at and timezone.now() > started_at + timezone.timedelta(minutes=test.time_limit):
        raise ValidationError({"time_limit": "Время прохождения теста истекло."})

    question_ids = [item["question"] for item in answers]
    duplicate_question_ids = sorted({question_id for question_id in question_ids if question_ids.count(question_id) > 1})
    if duplicate_question_ids:
        raise ValidationError({"answers": f"Обнаружены повторные ответы на вопросы: {duplicate_question_ids}."})

    expected_question_ids = {question.id for question in questions}
    submitted_question_ids = set(question_ids)
    unknown_question_ids = sorted(submitted_question_ids - expected_question_ids)
    if unknown_question_ids:
        raise ValidationError({"answers": f"Эти вопросы не относятся к выбранному тесту: {unknown_question_ids}."})

    missing_question_ids = sorted(expected_question_ids - submitted_question_ids)
    if missing_question_ids:
        raise ValidationError({"answers": f"Ответьте на все вопросы теста. Пропущены: {missing_question_ids}."})

    answer_map = {item["question"]: item["selected_option"] for item in answers}
    options_by_question = {
        question.id: {option.id: option for option in question.options.all()}
        for question in questions
    }
    invalid_options = [
        {"question": question_id, "selected_option": option_id}
        for question_id, option_id in answer_map.items()
        if option_id not in options_by_question.get(question_id, {})
    ]
    if invalid_options:
        raise ValidationError({"answers": {"invalid_options": invalid_options}})

    attempt = TestAttempt.objects.create(student=student, test=test, started_at=started_at or timezone.now())
    topic_stats = defaultdict(lambda: {"correct": 0, "total": 0, "topic": None})
    correct_count = 0
    total_count = len(questions)

    for question in questions:
        selected_option_id = answer_map.get(question.id)
        selected_option = options_by_question[question.id][selected_option_id]
        is_correct = bool(selected_option.is_correct)

        StudentAnswer.objects.create(
            attempt=attempt,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct,
        )

        topic_stats[question.topic_id]["topic"] = question.topic
        topic_stats[question.topic_id]["total"] += 1
        if is_correct:
            topic_stats[question.topic_id]["correct"] += 1
            correct_count += 1

    score = round((correct_count / total_count) * 100, 2) if total_count else 0
    attempt.score = score
    attempt.completed_at = timezone.now()
    attempt.is_completed = True
    attempt.save(update_fields=["score", "completed_at", "is_completed"])

    topic_results = []
    updated_progress = []
    for stats in topic_stats.values():
        progress = update_topic_progress(student, stats["topic"], stats["correct"], stats["total"], recalculate_overall=False)
        updated_progress.append(progress)
        topic_results.append({
            "topic": stats["topic"].title,
            "topic_id": stats["topic"].id,
            "correct": stats["correct"],
            "total": stats["total"],
            "mastery_percent": progress.mastery_percent,
            "level": progress.level,
        })

    update_student_progress(student)
    recommendations = generate_recommendations(student)

    return {
        "attempt_id": attempt.id,
        "score": score,
        "total_score": score,
        "topic_results": topic_results,
        "updated_progress": TopicProgressSerializer(updated_progress, many=True).data,
        "recommendations": RecommendationSerializer(recommendations, many=True).data,
    }
