import { ArrowRight } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import api from "../api/axios";

export default function Courses() {
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    api.get("/courses/").then((res) => setCourses(res.data)).catch(() => {});
  }, []);

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold">Курстар</h1>
        <p className="mt-2 text-slate-600">Окуучу бардык активдүү курстарды көрүп, темалар жана тесттер менен иштей алат.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {courses.map((course) => (
          <article key={course.id} className="panel">
            <h2 className="text-xl font-semibold">{course.title}</h2>
            <p className="mt-2 line-clamp-4 text-sm text-slate-600">{course.description}</p>
            <p className="mt-4 text-sm text-slate-500">Темалар: {course.topics?.length || 0}</p>
            <Link to={`/courses/${course.id}`} className="mt-5 inline-flex items-center gap-2 text-sm font-semibold text-primary">
              Курска өтүү <ArrowRight className="h-4 w-4" />
            </Link>
          </article>
        ))}
      </div>
    </div>
  );
}
