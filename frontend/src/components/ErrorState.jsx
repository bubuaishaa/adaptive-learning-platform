export default function ErrorState({ message = "Маалыматты жүктөөдө ката кетти.", onRetry }) {
  return (
    <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
      <p>{message}</p>
      {onRetry && (
        <button type="button" className="mt-3 rounded-lg bg-red-600 px-3 py-2 text-sm font-semibold text-white" onClick={onRetry}>
          Кайра аракет кылуу
        </button>
      )}
    </div>
  );
}
