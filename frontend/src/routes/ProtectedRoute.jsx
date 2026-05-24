import { Navigate, Outlet } from "react-router-dom";

import useAuthStore from "../store/authStore";

export default function ProtectedRoute({ roles }) {
  const { accessToken, user } = useAuthStore();

  if (!accessToken) {
    return <Navigate to="/login" replace />;
  }

  if (roles?.length && user && !roles.includes(user.role)) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
}
