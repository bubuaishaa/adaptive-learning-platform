import { ClipboardList } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import api from "../api/axios";
import LessonCard from "../components/LessonCard";

export default function CourseDetail() {
  const { id } = useParams();
  const [course, setCourse] = useState(null);
  const [tests, setTests] = useState([]);

  useEffect(() => {
    Promise.all([api.get(`/courses/${id}/`), api.get("/tests/")]).then(([courseRes, testsRes]) => {
      setCourse(courseRes.data);
      setTests(testsRes.data.filter((test) => Number(test.course) === Number(id)));
    }).catch(() => {});
  }, [id]);

  if (!course) {
    return <div className="panel">Жүктөлүүдө...</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">{course.title}</h1>
        <p className="mt-2 max-w-3xl text-slate-600">{course.description}</p>
      </div>
      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">Темалар жана сабактар</h2>
        {course.topics.map((topic) => (
          <div key={topic.id} className="panel">
            <h3 className="text-xl font-semibold">{topic.order}. {topic.title}</h3>
            <p className="mt-1 text-sm text-slate-600">{topic.description}</p>
            <div className="mt-4 grid gap-4 md:grid-cols-3">
              {topic.lessons.map((lesson) => <LessonCard key={lesson.id} lesson={lesson} />)}
            </div>
          </div>
        ))}
      </section>
      <section className="panel">
        <h2 className="text-2xl font-semibold">Тесттер</h2>
        <div className="mt-4 grid gap-3">
          {tests.map((test) => (
            <Link key={test.id} to={`/tests/${test.id}`} className="flex items-center justify-between rounded-lg border border-slate-200 p-4 hover:border-primary">
              <span>
                <span className="block font-semibold">{test.title}</span>
                <span className="text-sm text-slate-600">{test.description}</span>
              </span>
              <ClipboardList className="h-5 w-5 text-primary" />
            </Link>
          ))}
          {!tests.length && <p className="text-sm text-slate-500">Бул курс үчүн тест жок.</p>}
        </div>
      </section>
    </div>
  );
}
