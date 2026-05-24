import { Check, ExternalLink } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import api from "../api/axios";

export default function Recommendations() {
  const [recommendations, setRecommendations] = useState([]);
  const [learningPath, setLearningPath] = useState(null);

  const load = () => {
    Promise.all([api.get("/recommendations/my/"), api.get("/learning-path/my/")]).then(([recRes, pathRes]) => {
      setRecommendations(recRes.data);
      setLearningPath(pathRes.data);
    }).catch(() => {});
  };

  useEffect(() => {
    load();
  }, []);

  const completeStep = async (stepId) => {
    const { data } = await api.post(`/learning-path/steps/${stepId}/complete/`);
    setLearningPath(data);
    load();
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Сунушталган сабактар</h1>
        <p className="mt-2 text-slate-600">Сунуштар тема боюнча деңгээлге жараша түзүлөт жана жеке окуу траекториясына кошулат.</p>
      </div>
      <div className="grid gap-4 lg:grid-cols-[1fr_1fr]">
        <section className="panel">
          <h2 className="text-xl font-semibold">Сунуштоо механизми</h2>
          <div className="mt-4 space-y-3">
            {recommendations.map((item) => (
              <div key={item.id} className="rounded-lg border border-slate-200 p-4">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="font-semibold">{item.lesson}</p>
                    <p className="text-sm text-slate-500">{item.topic} · {item.lesson_type}</p>
                  </div>
                  <Link to={`/lessons/${item.lesson_id}`} className="text-primary" title="Сабакты ачуу">
                    <ExternalLink className="h-5 w-5" />
                  </Link>
                </div>
                <p className="mt-3 text-sm text-slate-600">{item.reason}</p>
              </div>
            ))}
            {!recommendations.length && <p className="text-sm text-slate-500">Тест тапшыргандан кийин сунуштар түзүлөт.</p>}
          </div>
        </section>
        <section className="panel">
          <h2 className="text-xl font-semibold">{learningPath?.title || "Жеке окуу траекториясы"}</h2>
          <div className="mt-4 space-y-3">
            {learningPath?.steps?.map((step) => (
              <div key={step.id} className="flex items-start justify-between gap-3 rounded-lg border border-slate-200 p-4">
                <div>
                  <p className="text-sm text-slate-500">Кадам {step.order} · {step.topic}</p>
                  <Link to={`/lessons/${step.lesson_id}`} className="font-semibold text-slate-900 hover:text-primary">{step.lesson}</Link>
                  <p className="mt-1 text-sm text-slate-600">Статус: {step.status}</p>
                </div>
                {step.status !== "completed" && (
                  <button type="button" className="btn-secondary" onClick={() => completeStep(step.id)} title="Аяктады деп белгилөө">
                    <Check className="h-4 w-4" />
                  </button>
                )}
              </div>
            ))}
            {!learningPath?.steps?.length && <p className="text-sm text-slate-500">Жеке траектория азырынча бош.</p>}
          </div>
        </section>
      </div>
    </div>
  );
}
