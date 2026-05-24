from django.core.management.base import BaseCommand

from apps.assessments.models import AnswerOption, Question, Test
from apps.courses.models import Course, Lesson, Topic
from apps.users.models import StudentProfile, TeacherProfile, User


class Command(BaseCommand):
    help = "Create demo data for the adaptive learning platform."

    def handle(self, *args, **options):
        admin = self._user("admin", "admin@example.com", "Admin", "User", User.Role.ADMIN, is_staff=True, is_superuser=True)
        teacher = self._user("teacher", "teacher@example.com", "Айгүл", "Мугалим", User.Role.TEACHER, is_staff=True)
        TeacherProfile.objects.get_or_create(user=teacher, defaults={"specialization": "Математика"})

        student1 = self._user("student1", "student1@example.com", "Бубуайша", "Абдыманапова", User.Role.STUDENT)
        student2 = self._user("student2", "student2@example.com", "Нурбек", "Окуучу", User.Role.STUDENT)
        StudentProfile.objects.get_or_create(user=student1, defaults={"grade_or_group": "ПМИ(б)-1-22"})
        StudentProfile.objects.get_or_create(user=student2, defaults={"grade_or_group": "ПМИ(б)-1-22"})

        course, _ = Course.objects.get_or_create(
            title="Математика",
            defaults={
                "description": "Негизги математикалык түшүнүктөр боюнча адаптивдүү курс.",
                "teacher": teacher,
            },
        )

        topics = []
        for order, title in enumerate(["Бөлчөктөр", "Пайыздар", "Сызыктуу теңдемелер"], start=1):
            topic, _ = Topic.objects.get_or_create(
                course=course,
                title=title,
                defaults={"description": f"{title} темасы боюнча теория жана практика.", "order": order},
            )
            topics.append(topic)
            self._lessons(topic)

        test, _ = Test.objects.get_or_create(
            course=course,
            title="Математика боюнча диагностикалык тест",
            defaults={"description": "Ар бир тема боюнча 5 суроодон турган баштапкы тест.", "time_limit": 30},
        )
        for topic in topics:
            self._questions(test, topic)

        self.stdout.write(self.style.SUCCESS("Seed data created."))
        self.stdout.write("Logins: admin/admin12345, teacher/teacher12345, student1/student12345, student2/student12345")

    def _user(self, username, email, first_name, last_name, role, is_staff=False, is_superuser=False):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "is_staff": is_staff,
                "is_superuser": is_superuser,
            },
        )
        if created:
            password = {
                User.Role.ADMIN: "admin12345",
                User.Role.TEACHER: "teacher12345",
                User.Role.STUDENT: "student12345",
            }[role]
            user.set_password(password)
            user.save()
        return user

    def _lessons(self, topic):
        data = [
            ("beginner", f"{topic.title}: баштапкы түшүндүрмө", "Негизги түшүнүктөр, жеңил мисалдар жана кадамдык түшүндүрүү."),
            ("reinforcement", f"{topic.title}: бекемдөөчү практика", "Кошумча мисалдар, текшерүүчү тапшырмалар жана практикалык көнүгүүлөр."),
            ("advanced", f"{topic.title}: татаал тапшырмалар", "Жогорку деңгээлдеги маселелер жана кийинки темага даярдык."),
        ]
        for order, (lesson_type, title, content) in enumerate(data, start=1):
            Lesson.objects.get_or_create(
                topic=topic,
                lesson_type=lesson_type,
                defaults={"title": title, "content": content, "order": order},
            )

    def _questions(self, test, topic):
        prompts = {
            "Бөлчөктөр": [
                ("1/2 + 1/4 = ?", "3/4", ["1/4", "2/4", "3/4", "4/4"]),
                ("2/3 - 1/3 = ?", "1/3", ["1/3", "2/3", "1/6", "3/3"]),
                ("1/5 * 2 = ?", "2/5", ["1/10", "2/5", "3/5", "5/2"]),
                ("3/4 бөлчөгүнүн ондук түрү кандай?", "0.75", ["0.25", "0.5", "0.75", "1.25"]),
                ("Кайсы бөлчөк 1ге барабар?", "4/4", ["1/4", "2/4", "3/4", "4/4"]),
            ],
            "Пайыздар": [
                ("100дүн 25% канча?", "25", ["10", "20", "25", "50"]),
                ("50дүн 10% канча?", "5", ["5", "10", "15", "20"]),
                ("0.5 канча пайыз?", "50%", ["5%", "25%", "50%", "100%"]),
                ("200дүн 15% канча?", "30", ["15", "20", "30", "45"]),
                ("Баасы 100 сом, арзандатуу 20%. Жаңы баа?", "80", ["70", "80", "90", "120"]),
            ],
            "Сызыктуу теңдемелер": [
                ("x + 3 = 7 болсо, x = ?", "4", ["3", "4", "7", "10"]),
                ("2x = 10 болсо, x = ?", "5", ["2", "5", "8", "10"]),
                ("x - 6 = 1 болсо, x = ?", "7", ["5", "6", "7", "8"]),
                ("3x + 1 = 10 болсо, x = ?", "3", ["2", "3", "4", "9"]),
                ("5x = 0 болсо, x = ?", "0", ["0", "1", "5", "-5"]),
            ],
        }
        for text, correct, options in prompts[topic.title]:
            question, _ = Question.objects.get_or_create(
                test=test,
                topic=topic,
                text=text,
                defaults={"difficulty": "easy"},
            )
            if question.options.exists():
                continue
            for option in options:
                AnswerOption.objects.create(question=question, text=option, is_correct=(option == correct))
