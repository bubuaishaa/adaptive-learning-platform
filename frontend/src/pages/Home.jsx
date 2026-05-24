import { ArrowRight, BrainCircuit, ChartNoAxesColumn, Route } from "lucide-react";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <section className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
      <div className="py-10">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary">Дипломдук практикалык платформа</p>
        <h1 className="mt-4 max-w-4xl text-4xl font-bold leading-tight text-slate-950 md:text-5xl">
          Жеке окуу траекториясын сунуштаган адаптивдүү онлайн билим берүү платформасы
        </h1>
        <p className="mt-5 max-w-2xl text-lg text-slate-600">
          Система тест жыйынтыгын талдап, ар бир тема боюнча өздөштүрүү пайызын эсептеп, окуучуга ылайыктуу сабактарды жана кийинки кадамдарды сунуштайт.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link to="/login" className="btn-primary">
            Кирүү <ArrowRight className="h-4 w-4" />
          </Link>
          <Link to="/register" className="btn-secondary">Катталуу</Link>
        </div>
      </div>
      <div className="panel">
        <div className="grid gap-4">
          <div className="rounded-lg bg-blue-50 p-4">
            <BrainCircuit className="h-7 w-7 text-primary" />
            <h2 className="mt-3 font-semibold">Тест жыйынтыгы</h2>
            <p className="mt-1 text-sm text-slate-600">Ар бир суроо белгилүү тема менен байланышат.</p>
          </div>
          <div className="rounded-lg bg-violet-50 p-4">
            <ChartNoAxesColumn className="h-7 w-7 text-accent" />
            <h2 className="mt-3 font-semibold">Өздөштүрүү деңгээли</h2>
            <p className="mt-1 text-sm text-slate-600">0-49% төмөн, 50-74% орточо, 75-100% жогорку деңгээл.</p>
          </div>
          <div className="rounded-lg bg-emerald-50 p-4">
            <Route className="h-7 w-7 text-emerald-600" />
            <h2 className="mt-3 font-semibold">Жеке окуу траекториясы</h2>
            <p className="mt-1 text-sm text-slate-600">Деңгээлге жараша beginner, reinforcement же advanced сабактар берилет.</p>
          </div>
        </div>
      </div>
    </section>
  );
}
