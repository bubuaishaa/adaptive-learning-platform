import { LogIn } from "lucide-react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";

import api from "../api/axios";
import useAuthStore from "../store/authStore";

export default function Login() {
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const setAuth = useAuthStore((state) => state.setAuth);
  const { register, handleSubmit, formState: { isSubmitting } } = useForm();

  const onSubmit = async (values) => {
    setError("");
    try {
      const { data } = await api.post("/auth/login/", values);
      setAuth(data);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.non_field_errors?.[0] || "Кирүү ишке ашкан жок.");
    }
  };

  return (
    <div className="mx-auto max-w-md">
      <div className="panel">
        <h1 className="text-2xl font-bold">Кирүү</h1>
        <p className="mt-2 text-sm text-slate-600">Логин же email жана сырсөз киргизиңиз.</p>
        {error && <div className="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</div>}
        <form onSubmit={handleSubmit(onSubmit)} className="mt-6 space-y-4">
          <div>
            <label className="text-sm font-medium">Username же email</label>
            <input className="input mt-1" {...register("username", { required: true })} />
          </div>
          <div>
            <label className="text-sm font-medium">Сырсөз</label>
            <input type="password" className="input mt-1" {...register("password", { required: true })} />
          </div>
          <button className="btn-primary w-full" type="submit" disabled={isSubmitting}>
            <LogIn className="h-4 w-4" /> Кирүү
          </button>
        </form>
        <p className="mt-4 text-sm text-slate-600">
          Аккаунт жокпу? <Link className="font-semibold text-primary" to="/register">Катталуу</Link>
        </p>
      </div>
    </div>
  );
}
