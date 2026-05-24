import { BookOpen, ClipboardList, UsersRound } from "lucide-react";
import { useEffect, useState } from "react";

import api from "../api/axios";
import ErrorState from "../components/ErrorState";
import LoadingState from "../components/LoadingState";
import PageHeader from "../components/PageHeader";

export default function AdminDashboard() {
  const [stats, setStats] = useState({ users: 0, courses: 0, tests: 0 });
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      const [usersRes, coursesRes, testsRes] = await Promise.all([api.get("/users/"), api.get("/courses/"), api.get("/tests/")]);
      setUsers(usersRes.data);
      setStats({ users: usersRes.data.length, courses: coursesRes.data.length, tests: testsRes.data.length });
    } catch {
      setError("Админ маалыматтарын жүктөөдө ката кетти.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const updateUser = async (user, patch) => {
    await api.patch(`/users/${user.id}/`, patch);
    load();
  };

  if (loading) {
    return <LoadingState />;
  }
  if (error) {
    return <ErrorState message={error} onRetry={load} />;
  }

  return (
    <div className="space-y-6">
      <PageHeader title="Админ панели" description="Колдонуучулар, курстар жана тесттер боюнча жалпы статистика." />
      <div className="grid gap-4 md:grid-cols-3">
        <Metric icon={<UsersRound className="h-6 w-6 text-primary" />} label="Колдонуучулар" value={stats.users} />
        <Metric icon={<BookOpen className="h-6 w-6 text-emerald-600" />} label="Курстар" value={stats.courses} />
        <Metric icon={<ClipboardList className="h-6 w-6 text-accent" />} label="Тесттер" value={stats.tests} />
      </div>
      <section className="panel overflow-x-auto">
        <h2 className="text-xl font-semibold">Колдонуучулар</h2>
        <table className="mt-4 w-full text-left text-sm">
          <thead className="bg-slate-50 text-slate-600">
            <tr>
              <th className="p-3">Username</th>
              <th className="p-3">Email</th>
              <th className="p-3">Роль</th>
              <th className="p-3">Активдүү</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id} className="border-t border-slate-100">
                <td className="p-3 font-medium">{user.username}</td>
                <td className="p-3">{user.email}</td>
                <td className="p-3">
                  <select className="input max-w-36" value={user.role} onChange={(event) => updateUser(user, { role: event.target.value })}>
                    <option value="student">student</option>
                    <option value="teacher">teacher</option>
                    <option value="admin">admin</option>
                  </select>
                </td>
                <td className="p-3">
                  <label className="inline-flex items-center gap-2">
                    <input type="checkbox" checked={user.is_active} onChange={(event) => updateUser(user, { is_active: event.target.checked })} />
                    {user.is_active ? "Ооба" : "Жок"}
                  </label>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}

function Metric({ icon, label, value }) {
  return <div className="panel">{icon}<p className="mt-3 text-sm text-slate-500">{label}</p><p className="text-3xl font-bold">{value}</p></div>;
}
