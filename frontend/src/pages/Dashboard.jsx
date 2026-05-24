import { BookOpen, ClipboardCheck, Route, Shield, Users } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";

import api from "../api/axios";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import LoadingState from "../components/LoadingState";
import PageHeader from "../components/PageHeader";
import ProgressChart from "../components/ProgressChart";
import useAuthStore from "../store/authStore";

export default function Dashboard() {
  const user = useAuthStore((state) => state.user);
  const [data, setData] = useState({ courses: [], progress: { summary: null, topics: [] }, recommendations: [], attempts: [], users: [], tests: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      if (user?.role === "student") {
        const [coursesRes, progressRes, recRes, attemptsRes] = await Promise.all([
          api.get("/courses/"),
          api.get("/progress/my/"),
          api.get("/recommendations/my/"),
          api.get("/attempts/"),
        ]);
        setData({ courses: coursesRes.data, progress: progressRes.data, recommendations: recRes.data.slice(0, 3), attempts: attemptsRes.data.slice(0, 3), users: [], tests: [] });
      } else if (user?.role === "teacher") {
        const [coursesRes, studentsRes, attemptsRes] = await Promise.all([
          api.get("/courses/"),
          api.get("/users/students/"),
          api.get("/attempts/"),
        ]);
        setData({ courses: coursesRes.data, progress: { summary: null, topics: [] }, recommendations: [], attempts: attemptsRes.data.slice(0, 5), users: studentsRes.data, tests: [] });
      } else {
        const [usersRes, coursesRes, testsRes] = await Promise.all([
          api.get("/users/"),
          api.get("/courses/"),
          api.get("/tests/"),
        ]);
        setData({ courses: coursesRes.data, progress: { summary: null, topics: [] }, recommendations: [], attempts: [], users: usersRes.data, tests: testsRes.data });
      }
    } catch {
      setError("Dashboard маалыматтарын жүктөөдө ката кетти.");
    } finally {
      setLoading(false);
    }
  }, [user?.role]);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) {
    return <LoadingState />;
  }

  if (error) {
    return <ErrorState message={error} onRetry={load} />;
  }

  if (user?.role === "teacher") {
    return <TeacherSummary data={data} user={user} />;
  }

  if (user?.role === "admin") {
    return <AdminSummary data={data} user={user} />;
  }

  return <StudentSummary data={data} user={user} />;
}

function StudentSummary({ data, user }) {
  return (
    <div className="space-y-6">
      <PageHeader title={`Салам, ${user?.first_name || user?.username}`} description="Курстар, акыркы тесттер, прогресс жана сунуштар бир жерге чогултулган." />
      <div className="grid gap-4 md:grid-cols-3">
        <Metric icon={<BookOpen className="h-6 w-6 text-primary" />} label="Менин курстарым" value={data.courses.length} />
        <Metric icon={<ClipboardCheck className="h-6 w-6 text-emerald-600" />} label="Аяктаган тесттер" value={data.progress.summary?.completed_tests || 0} />
        <Metric icon={<Route className="h-6 w-6 text-accent" />} label="Жалпы прогресс" value={`${data.progress.summary?.overall_percent || 0}%`} />
      </div>
      <div className="grid gap-6 lg:grid-cols-[1.4fr_0.8fr]">
        <div className="panel">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-xl font-semibold">Тема боюнча прогресс</h2>
            <Link to="/progress" className="text-sm font-semibold text-primary">Толук көрүү</Link>
          </div>
          {data.progress.topics.length ? <ProgressChart data={data.progress.topics} /> : <EmptyState title="Прогресс жок" text="Тест тапшыргандан кийин диаграмма пайда болот." />}
        </div>
        <div className="space-y-4">
          <SideList title="Сунушталган сабактар" empty="Тест тапшыргандан кийин сунуштар чыгат." items={data.recommendations} render={(item) => (
            <Link key={item.id} to={`/lessons/${item.lesson_id}`} className="block rounded-lg border border-slate-200 p-3 hover:border-primary">
              <p className="font-semibold">{item.lesson}</p>
              <p className="text-sm text-slate-600">{item.topic}</p>
            </Link>
          )} />
          <SideList title="Акыркы тест жыйынтыгы" empty="Азырынча тест жыйынтыгы жок." items={data.attempts} render={(attempt) => (
            <div key={attempt.id} className="rounded-lg bg-slate-50 p-3">
              <p className="font-semibold">{attempt.test_title}</p>
              <p className="text-sm text-slate-600">Жыйынтык: {attempt.score}%</p>
            </div>
          )} />
        </div>
      </div>
    </div>
  );
}

function TeacherSummary({ data, user }) {
  return (
    <div className="space-y-6">
      <PageHeader title={`Мугалим панели: ${user?.first_name || user?.username}`} description="Бул dashboard teacher-only endpointтерди гана чакырат." actions={<Link className="btn-primary" to="/teacher">Башкаруу панелине өтүү</Link>} />
      <div className="grid gap-4 md:grid-cols-3">
        <Metric icon={<BookOpen className="h-6 w-6 text-primary" />} label="Менин курстарым" value={data.courses.length} />
        <Metric icon={<Users className="h-6 w-6 text-emerald-600" />} label="Менин окуучуларым" value={data.users.length} />
        <Metric icon={<ClipboardCheck className="h-6 w-6 text-accent" />} label="Тест аракеттери" value={data.attempts.length} />
      </div>
      <SideList title="Акыркы аракеттер" empty="Сиздин курстарыңыз боюнча аракеттер жок." items={data.attempts} render={(attempt) => (
        <div key={attempt.id} className="rounded-lg border border-slate-200 p-3">
          <p className="font-semibold">{attempt.test_title}</p>
          <p className="text-sm text-slate-600">{attempt.score}%</p>
        </div>
      )} />
    </div>
  );
}

function AdminSummary({ data, user }) {
  return (
    <div className="space-y-6">
      <PageHeader title={`Админ панели: ${user?.first_name || user?.username}`} description="Системанын жалпы статистикасы." actions={<Link className="btn-primary" to="/admin">Админ барагына өтүү</Link>} />
      <div className="grid gap-4 md:grid-cols-3">
        <Metric icon={<Shield className="h-6 w-6 text-primary" />} label="Колдонуучулар" value={data.users.length} />
        <Metric icon={<BookOpen className="h-6 w-6 text-emerald-600" />} label="Курстар" value={data.courses.length} />
        <Metric icon={<ClipboardCheck className="h-6 w-6 text-accent" />} label="Тесттер" value={data.tests.length} />
      </div>
    </div>
  );
}

function Metric({ icon, label, value }) {
  return (
    <div className="panel">
      {icon}
      <p className="mt-3 text-sm text-slate-500">{label}</p>
      <p className="text-3xl font-bold">{value}</p>
    </div>
  );
}

function SideList({ title, empty, items, render }) {
  return (
    <div className="panel">
      <h2 className="text-xl font-semibold">{title}</h2>
      <div className="mt-4 space-y-3">
        {items.length ? items.map(render) : <EmptyState title="Маалымат жок" text={empty} />}
      </div>
    </div>
  );
}
