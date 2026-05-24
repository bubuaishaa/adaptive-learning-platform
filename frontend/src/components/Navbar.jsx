import { BookOpen, ChartNoAxesColumn, LogOut, Route, Shield, UserRoundCog } from "lucide-react";
import { Link, NavLink, useNavigate } from "react-router-dom";

import useAuthStore from "../store/authStore";

const navClass = ({ isActive }) =>
  `inline-flex items-center gap-1 rounded-lg px-3 py-2 text-sm font-medium transition ${isActive ? "bg-blue-50 text-primary" : "text-slate-600 hover:bg-slate-100"}`;

export default function Navbar() {
  const { accessToken, user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-4 py-3">
        <Link to="/" className="flex items-center gap-2 text-base font-bold text-slate-900">
          <BookOpen className="h-5 w-5 text-primary" />
          Adaptive Learning
        </Link>
        <nav className="flex flex-wrap items-center gap-1">
          {accessToken ? (
            <>
              <NavLink to="/dashboard" className={navClass}>Башкы панель</NavLink>
              <NavLink to="/courses" className={navClass}>Курстар</NavLink>
              <NavLink to="/progress" className={navClass}>
                <ChartNoAxesColumn className="h-4 w-4" /> Прогресс
              </NavLink>
              <NavLink to="/recommendations" className={navClass}>
                <Route className="h-4 w-4" /> Сунуштар
              </NavLink>
              {["teacher", "admin"].includes(user?.role) && <NavLink to="/teacher" className={navClass}><UserRoundCog className="h-4 w-4" /> Мугалим</NavLink>}
              {user?.role === "admin" && <NavLink to="/admin" className={navClass}><Shield className="h-4 w-4" /> Админ</NavLink>}
              <button type="button" onClick={handleLogout} className="btn-secondary">
                <LogOut className="h-4 w-4" /> Чыгуу
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login" className={navClass}>Кирүү</NavLink>
              <Link to="/register" className="btn-primary">Катталуу</Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
