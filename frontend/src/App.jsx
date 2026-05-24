import { lazy, Suspense } from "react";
import { Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import LoadingState from "./components/LoadingState";
import ProtectedRoute from "./routes/ProtectedRoute";

const AdminDashboard = lazy(() => import("./pages/AdminDashboard"));
const CourseDetail = lazy(() => import("./pages/CourseDetail"));
const Courses = lazy(() => import("./pages/Courses"));
const Dashboard = lazy(() => import("./pages/Dashboard"));
const Home = lazy(() => import("./pages/Home"));
const LessonDetail = lazy(() => import("./pages/LessonDetail"));
const Login = lazy(() => import("./pages/Login"));
const Progress = lazy(() => import("./pages/Progress"));
const Recommendations = lazy(() => import("./pages/Recommendations"));
const Register = lazy(() => import("./pages/Register"));
const TeacherDashboard = lazy(() => import("./pages/TeacherDashboard"));
const TestPage = lazy(() => import("./pages/TestPage"));

export default function App() {
  return (
    <Suspense fallback={<div className="mx-auto max-w-7xl px-4 py-8"><LoadingState /></div>}>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/courses" element={<Courses />} />
            <Route path="/courses/:id" element={<CourseDetail />} />
            <Route path="/lessons/:id" element={<LessonDetail />} />
            <Route path="/tests/:id" element={<TestPage />} />
            <Route path="/progress" element={<Progress />} />
            <Route path="/recommendations" element={<Recommendations />} />
          </Route>
          <Route element={<ProtectedRoute roles={["teacher", "admin"]} />}>
            <Route path="/teacher" element={<TeacherDashboard />} />
          </Route>
          <Route element={<ProtectedRoute roles={["admin"]} />}>
            <Route path="/admin" element={<AdminDashboard />} />
          </Route>
        </Route>
      </Routes>
    </Suspense>
  );
}
