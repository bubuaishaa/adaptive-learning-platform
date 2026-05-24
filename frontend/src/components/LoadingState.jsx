export default function LoadingState({ text = "Жүктөлүүдө..." }) {
  return (
    <div className="panel text-sm text-slate-600">
      {text}
    </div>
  );
}
