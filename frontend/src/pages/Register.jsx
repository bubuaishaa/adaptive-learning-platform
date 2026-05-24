import { UserPlus } from "lucide-react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";

import api from "../api/axios";

export default function Register() {
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { register, handleSubmit, formState: { isSubmitting } } = useForm({
    defaultValues: { role: "student" },
  });

  const onSubmit = async (values) => {
    setError("");
    try {
      await api.post("/auth/register/", values);
      navigate("/login");
    } catch (err) {
      setError("Катталуу учурунда ката кетти. Username/email уникалдуу болушу керек.");
    }
  };

  return (
    <div className="mx-auto max-w-xl">
      <div className="panel">
        <h1 className="text-2xl font-bold">Катталуу</h1>
        <p className="mt-2 text-sm text-slate-600">Жаңы окуучу аккаунтун түзүү.</p>
        {error && <div className="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</div>}
        <form onSubmit={handleSubmit(onSubmit)} className="mt-6 grid gap-4 md:grid-cols-2">
          <div>
            <label className="text-sm font-medium">Username</label>
            <input className="input mt-1" {...register("username", { required: true })} />
          </div>
          <div>
            <label className="text-sm font-medium">Email</label>
            <input type="email" className="input mt-1" {...register("email", { required: true })} />
          </div>
          <div>
            <label className="text-sm font-medium">Аты</label>
            <input className="input mt-1" {...register("first_name")} />
          </div>
          <div>
            <label className="text-sm font-medium">Фамилиясы</label>
            <input className="input mt-1" {...register("last_name")} />
          </div>
          <div className="md:col-span-2">
            <label className="text-sm font-medium">Сырсөз</label>
            <input type="password" className="input mt-1" {...register("password", { required: true, minLength: 8 })} />
          </div>
          <input type="hidden" {...register("role")} />
          <button className="btn-primary md:col-span-2" type="submit" disabled={isSubmitting}>
            <UserPlus className="h-4 w-4" /> Катталуу
          </button>
        </form>
        <p className="mt-4 text-sm text-slate-600">
          Аккаунт барбы? <Link className="font-semibold text-primary" to="/login">Кирүү</Link>
        </p>
      </div>
    </div>
  );
}
