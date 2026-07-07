import * as Progress from '@radix-ui/react-progress';
import { ShieldCheck } from 'lucide-react';

import RiskBadge, { riskTone } from './RiskBadge.jsx';

const barStyles = {
  safe: 'bg-emerald-500',
  caution: 'bg-amber-500',
  medium: 'bg-orange-500',
  high: 'bg-red-500',
};

export default function TrustScoreCard({ result }) {
  const tone = riskTone(result.trust_score);

  return (
    <section className="card p-5">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <div className="flex items-center gap-2 text-sm font-semibold text-zinc-600">
            <ShieldCheck className="h-4 w-4" aria-hidden="true" />
            Trust Score
          </div>
          <div className="mt-3 flex items-end gap-3">
            <span className="text-5xl font-semibold tracking-normal text-zinc-950">{result.trust_score}</span>
            <span className="pb-2 text-sm font-medium text-zinc-500">/100</span>
          </div>
        </div>
        <RiskBadge score={result.trust_score} label={result.risk_level} />
      </div>
      <Progress.Root className="mt-5 h-3 overflow-hidden rounded-full bg-zinc-100" value={result.trust_score}>
        <Progress.Indicator
          className={`h-full rounded-full transition-all ${barStyles[tone]}`}
          style={{ transform: `translateX(-${100 - result.trust_score}%)` }}
        />
      </Progress.Root>
      <p className="mt-4 text-sm leading-6 text-zinc-600">{result.summary}</p>
    </section>
  );
}
