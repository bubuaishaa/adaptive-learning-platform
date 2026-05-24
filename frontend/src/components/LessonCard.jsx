import { ArrowRight, BookOpen } from "lucide-react";
import { Link } from "react-router-dom";

const labels = {
  beginner: "Баштапкы",
  reinforcement: "Бекемдөө",
  advanced: "Жогорку",
};

const colors = {
  beginner: "bg-amber-50 text-amber-700",
  reinforcement: "bg-blue-50 text-blue-700",
  advanced: "bg-violet-50 text-violet-700",
};

export default function LessonCard({ lesson }) {
  return (
    <article className="rounded-lg border border-slate-200 bg-white p-4">
      <div className="mb-3 flex items-start justify-between gap-3">
        <BookOpen className="mt-1 h-5 w-5 text-primary" />
        <span className={`badge ${colors[lesson.lesson_type] || "bg-slate-100 text-slate-700"}`}>
          {labels[lesson.lesson_type] || lesson.lesson_type}
        </span>
      </div>
      <h3 className="font-semibold text-slate-900">{lesson.title}</h3>
      <p className="mt-2 line-clamp-3 text-sm text-slate-600">{lesson.content}</p>
      <Link className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-primary" to={`/lessons/${lesson.id}`}>
        Сабакты ачуу <ArrowRight className="h-4 w-4" />
      </Link>
    </article>
  );
}
