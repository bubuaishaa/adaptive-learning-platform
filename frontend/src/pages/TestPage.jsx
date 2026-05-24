import { CheckCircle2 } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";

import api from "../api/axios";

const levelLabel = {
  low: "Төмөн деңгээл",
  medium: "Орточо деңгээл",
  high: "Жогорку деңгээл",
};

export default function TestPage() {
  const { id } = useParams();
  const [test, setTest] = useState(null);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    api.get(`/tests/${id}/`).then((res) => setTest(res.data)).catch(() => {});
  }, [id]);

  const isComplete = useMemo(() => test?.questions?.every((question) => answers[question.id]), [answers, test]);

  const submit = async () => {
    setSubmitting(true);
    const payload = {
      answers: Object.entries(answers).map(([question, selectedOption]) => ({
        question: Number(question),
        selected_option: Number(selectedOption),
      })),
    };
    try {
      const { data } = await api.post(`/tests/${id}/submit/`, payload);
      setResult(data);
    } finally {
      setSubmitting(false);
    }
  };

  if (!test) {
    return <div className="panel">Жүктөлүүдө...</div>;
  }

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <div>
        <h1 className="text-3xl font-bold">{test.title}</h1>
        <p className="mt-2 text-slate-600">{test.description}</p>
      </div>
      {!result && (
        <div className="space-y-4">
          {test.questions.map((question, index) => (
            <div key={question.id} className="panel">
              <p className="text-sm font-semibold text-primary">{index + 1}-суроо · {question.topic_title}</p>
              <h2 className="mt-2 text-lg font-semibold">{question.text}</h2>
              <div className="mt-4 grid gap-2">
                {question.options.map((option) => (
                  <label key={option.id} className={`flex cursor-pointer items-center gap-3 rounded-lg border p-3 text-sm ${Number(answers[question.id]) === option.id ? "border-primary bg-blue-50" : "border-slate-200 bg-white"}`}>
                    <input
                      type="radio"
                      name={`question-${question.id}`}
                      value={option.id}
                      checked={Number(answers[question.id]) === option.id}
                      onChange={() => setAnswers((current) => ({ ...current, [question.id]: option.id }))}
                    />
                    {option.text}
                  </label>
                ))}
              </div>
            </div>
          ))}
          <button className="btn-primary" type="button" onClick={submit} disabled={!isComplete || submitting}>
            <CheckCircle2 className="h-4 w-4" /> Тестти тапшыруу
          </button>
        </div>
      )}
      {result && (
        <div className="space-y-6">
          <div className="panel">
            <p className="text-sm text-slate-500">Жалпы жыйынтык</p>
            <p className="mt-2 text-4xl font-bold text-primary">{result.score}%</p>
          </div>
          <div className="panel">
            <h2 className="text-xl font-semibold">Тема боюнча жыйынтыктар</h2>
            <div className="mt-4 overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-50 text-slate-600">
                  <tr>
                    <th className="p-3">Тема</th>
                    <th className="p-3">Туура</th>
                    <th className="p-3">Өздөштүрүү</th>
                    <th className="p-3">Деңгээл</th>
                  </tr>
                </thead>
                <tbody>
                  {result.topic_results.map((item) => (
                    <tr key={item.topic_id} className="border-t border-slate-100">
                      <td className="p-3 font-medium">{item.topic}</td>
                      <td className="p-3">{item.correct}/{item.total}</td>
                      <td className="p-3">{item.mastery_percent}%</td>
                      <td className="p-3">{levelLabel[item.level]}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          <div className="panel">
            <h2 className="text-xl font-semibold">Сунушталган материалдар</h2>
            <div className="mt-4 grid gap-3">
              {result.recommendations.slice(0, 6).map((item) => (
                <Link key={item.id} to={`/lessons/${item.lesson_id}`} className="rounded-lg border border-slate-200 p-4 hover:border-primary">
                  <p className="font-semibold">{item.lesson}</p>
                  <p className="mt-1 text-sm text-slate-600">{item.reason}</p>
                </Link>
              ))}
            </div>
            <Link to="/recommendations" className="btn-primary mt-5">Сунушталган материалдарды көрүү</Link>
          </div>
        </div>
      )}
    </div>
  );
}
