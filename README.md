# Adaptive Learning Platform

Дипломная тема: “Адаптивная онлайн-образовательная платформа, предлагающая персонализированную траекторию обучения”.

Студент: Абдыманапова Бубуайша Алтынбековна  
Группа: ПМИ(б)-1-22  
Направление: Прикладная математика и информатика

## Назначение

Проект демонстрирует MVP адаптивной образовательной платформы. Это не просто сайт с курсами: студент проходит тест, backend считает освоение по темам, обновляет общий прогресс и генерирует рекомендации с индивидуальной learning path.

## Технологии

Backend: Python, Django 5, Django REST Framework, SimpleJWT, PostgreSQL, django-cors-headers, drf-spectacular.  
Frontend: React 18, Vite, Tailwind CSS, React Router, Axios, Zustand, React Hook Form, Recharts.  
DevOps: Docker, docker-compose, `.env`.

## Структура

```text
backend/
  config/
  apps/users/
  apps/courses/
  apps/assessments/
  apps/progress/
  apps/recommendations/
  seeds/
frontend/
  src/api/
  src/store/
  src/routes/
  src/components/
  src/pages/
docker-compose.yml
.env.example
```

## Запуск через Docker

```bash
docker-compose up --build
docker-compose exec backend python manage.py seed_data
```

Backend: http://localhost:8000  
Frontend: http://localhost:5173  
Swagger UI: http://localhost:8000/api/docs/

## Локальный запуск

Backend:

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Проверки

Backend:

```bash
cd backend
python manage.py check
python manage.py test
```

Frontend:

```bash
cd frontend
npm run lint
npm run build
```

## Demo логины

| Роль | Username | Password |
| --- | --- | --- |
| admin | admin | admin12345 |
| teacher | teacher | teacher12345 |
| student | student1 | student12345 |
| student | student2 | student12345 |

## Роли

`student`: видит курсы, проходит тесты, видит только свои attempts/progress/recommendations/learning path.  
`teacher`: управляет только своими курсами, темами, уроками, тестами и вопросами; видит попытки студентов только по своим курсам.  
`admin`: видит всё, может менять роль и активность пользователей.

## Основные API

Auth: `POST /api/auth/register/`, `POST /api/auth/login/`, `POST /api/auth/token/refresh/`, `GET /api/auth/me/`

Users: `GET /api/users/`, `GET/PATCH /api/users/{id}/`, `GET /api/users/students/`, `GET /api/users/teachers/`

Courses: `GET/POST /api/courses/`, `GET/PATCH/DELETE /api/courses/{id}/`, `GET/POST /api/topics/`, `GET/PATCH/DELETE /api/topics/{id}/`, `GET/POST /api/lessons/`, `GET/PATCH/DELETE /api/lessons/{id}/`

Assessments: `GET/POST /api/tests/`, `GET/PATCH/DELETE /api/tests/{id}/`, `POST /api/tests/{id}/submit/`, `GET /api/attempts/`, `GET/POST /api/questions/`, `GET/PATCH/DELETE /api/questions/{id}/`, `GET/POST /api/answer-options/`

Progress: `GET /api/progress/my/`, `GET /api/progress/topics/`, `GET /api/progress/summary/`, `GET /api/progress/student/{id}/`

Recommendations: `GET /api/recommendations/my/`, `POST /api/recommendations/regenerate/`, `GET /api/learning-path/my/`, `POST /api/learning-path/steps/{id}/complete/`

## Adaptive Algorithm

Каждый `Question` связан с `Topic`. После submit backend проверяет ответы, группирует результат по темам и считает topic score:

```text
topic_score = correct_answers_for_topic / total_questions_for_topic * 100
```

Чтобы прогресс не перезаписывался случайной последней попыткой, `mastery_percent` считается как weighted recent average по последним трём topic-level попыткам:

```text
mastery = (score1 * 1 + score2 * 2 + score3 * 3) / (1 + 2 + 3)
```

Новые попытки имеют больший вес, старые результаты стабилизируют оценку. Общий прогресс учитывает темы курса, с которым студент уже работал: непройденные темы считаются как 0%.

Деңгээл шкаласы:

- `low`: 0-49%, beginner lessons.
- `medium`: 50-74%, reinforcement lessons.
- `high`: 75-100%, advanced lessons или следующий topic.

`POST /api/tests/{id}/submit/`:

1. Валидирует, что тест не пустой.
2. Проверяет, что все вопросы относятся к тесту.
3. Проверяет дубли и неполные ответы.
4. Проверяет, что selected option принадлежит своему вопросу.
5. Обновляет `TestAttempt`, `StudentAnswer`, `TopicProgress`, `StudentProgress`.
6. Генерирует `Recommendation` и `LearningPathStep`.

## User Flow

1. Student логинится и открывает курс.
2. Student проходит диагностический тест.
3. Backend возвращает score и topic results.
4. Страница progress показывает диаграмму Recharts.
5. Страница recommendations показывает персональные уроки и learning path.
6. Teacher через dashboard создаёт курсы, темы, уроки, тесты, вопросы и варианты.
7. Admin управляет пользователями.

## Database модели

`users`: Custom `User`, `StudentProfile`, `TeacherProfile`.  
`courses`: `Course`, `Topic`, `Lesson`.  
`assessments`: `Test`, `Question`, `AnswerOption`, `TestAttempt`, `StudentAnswer`.  
`progress`: `TopicProgress`, `StudentProgress`.  
`recommendations`: `Recommendation`, `LearningPath`, `LearningPathStep`.

## Ограничения

Это дипломный MVP, а не production LMS. В проекте нет полноценной записи на курсы, оплаты, email verification, httpOnly-cookie auth, аудита действий и сложной аналитики. JWT хранится во frontend localStorage через Zustand persist: это удобно для демонстрации, но в production лучше использовать httpOnly cookies и более строгую CSRF/XSS модель.
