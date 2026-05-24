import { useEffect, useState } from "react";

import api from "../api/axios";
import ProgressChart from "../components/ProgressChart";

const levelStyles = {
  low: "bg-red-50 text-red-700",
  medium: "bg-amber-50 text-amber-700",
  high: "bg-emerald-50 text-emerald-700",
};

const levelLabels = {
  low: "Төмөн деңгээл",
  medium: "Орточо деңгээл",
  high: "Жогорку деңгээл",
};

export default function Progress() {
  const [progress, setProgress] = useState({ summary: null, topics: [] });

  useEffect(() => {
    api.get("/progress/my/").then((res) => setProgress(res.data)).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Прогресс</h1>
        <p className="mt-2 text-slate-600">Тест жыйынтыктарынын негизинде тема боюнча өздөштүрүү пайызы эсептелет.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        <div className="panel">
          <p className="text-sm text-slate-500">Жалпы пайыз</p>
          <p className="mt-2 text-3xl font-bold">{progress.summary?.overall_percent || 0}%</p>
        </div>
        <div className="panel">
          <p className="text-sm text-slate-500">Жалпы деңгээл</p>
          <span className={`badge mt-3 ${levelStyles[progress.summary?.overall_level] || "bg-slate-100 text-slate-700"}`}>
            {levelLabels[progress.summary?.overall_level] || "Маалымат жок"}
          </span>
        </div>
        <div className="panel">
          <p className="text-sm text-slate-500">Аяктаган тесттер</p>
          <p className="mt-2 text-3xl font-bold">{progress.summary?.completed_tests || 0}</p>
        </div>
      </div>
      <div className="panel">
        <h2 className="text-xl font-semibold">Диаграмма</h2>
        <ProgressChart data={progress.topics} />
      </div>
      <div className="panel overflow-x-auto">
        <h2 className="text-xl font-semibold">Тема деталдары</h2>
        <table className="mt-4 w-full text-left text-sm">
          <thead className="bg-slate-50 text-slate-600">
            <tr>
              <th className="p-3">Тема</th>
              <th className="p-3">Курс</th>
              <th className="p-3">Өздөштүрүү</th>
              <th className="p-3">Деңгээл</th>
            </tr>
          </thead>
          <tbody>
            {progress.topics.map((item) => (
              <tr key={item.id} className="border-t border-slate-100">
                <td className="p-3 font-medium">{item.topic}</td>
                <td className="p-3">{item.course}</td>
                <td className="p-3">{item.mastery_percent}%</td>
                <td className="p-3"><span className={`badge ${levelStyles[item.level]}`}>{levelLabels[item.level]}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
