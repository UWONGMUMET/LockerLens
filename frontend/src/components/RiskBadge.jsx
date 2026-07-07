const styles = {
  safe: 'border-emerald-200 bg-emerald-50 text-emerald-700',
  caution: 'border-amber-200 bg-amber-50 text-amber-700',
  medium: 'border-orange-200 bg-orange-50 text-orange-700',
  high: 'border-red-200 bg-red-50 text-red-700',
};

export function riskTone(score = 0) {
  if (score >= 85) return 'safe';
  if (score >= 70) return 'caution';
  if (score >= 45) return 'medium';
  return 'high';
}

export default function RiskBadge({ score, label }) {
  const tone = riskTone(score);
  return (
    <span className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold ${styles[tone]}`}>
      {label}
    </span>
  );
}
