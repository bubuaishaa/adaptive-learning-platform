import { ArrowLeft } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import api from "../api/axios";

const labels = {
  beginner: "Баштапкы деңгээл",
  reinforcement: "Бекемдөөчү материал",
  advanced: "Жогорку деңгээл",
};

export default function LessonDetail() {
  const { id } = useParams();
  const [lesson, setLesson] = useState(null);

  useEffect(() => {
    api.get(`/lessons/${id}/`).then((res) => setLesson(res.data)).catch(() => {});
  }, [id]);

  if (!lesson) {
    return <div className="panel">Жүктөлүүдө...</div>;
  }

  return (
    <article className="mx-auto max-w-3xl">
      <Link to={`/courses/${lesson.course_id}`} className="mb-5 inline-flex items-center gap-2 text-sm font-semibold text-primary">
        <ArrowLeft className="h-4 w-4" /> Курска кайтуу
      </Link>
      <div className="panel">
        <span className="badge bg-blue-50 text-blue-700">{labels[lesson.lesson_type]}</span>
        <h1 className="mt-4 text-3xl font-bold">{lesson.title}</h1>
        <p className="mt-2 text-sm text-slate-500">Тема: {lesson.topic_title}</p>
        <div className="prose prose-slate mt-6 max-w-none whitespace-pre-line">{lesson.content}</div>
        {lesson.video_url && (
          <a className="btn-secondary mt-6" href={lesson.video_url} target="_blank" rel="noreferrer">Видео көрүү</a>
        )}
      </div>
    </article>
  );
}
