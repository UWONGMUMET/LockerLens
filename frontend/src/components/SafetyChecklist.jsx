import { CheckCircle2 } from 'lucide-react';

import { safetyChecklist } from '../data/content.js';

export default function SafetyChecklist({ items = safetyChecklist }) {
  return (
    <div className="grid gap-3">
      {items.map((item) => (
        <div key={item} className="flex gap-3 rounded-lg border border-zinc-200 bg-white p-4 text-sm leading-6 text-zinc-700">
          <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-emerald-600" aria-hidden="true" />
          <span>{item}</span>
        </div>
      ))}
    </div>
  );
}
