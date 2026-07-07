import { AlertTriangle, CheckCircle2, CircleHelp } from 'lucide-react';

const statusStyles = {
  passed: 'border-emerald-200 bg-emerald-50 text-emerald-800',
  warning: 'border-amber-200 bg-amber-50 text-amber-800',
  missing: 'border-amber-200 bg-amber-50 text-amber-800',
};

const statusIcons = {
  passed: CheckCircle2,
  warning: AlertTriangle,
  missing: CircleHelp,
};

export default function SafeApplyChecklistCard({ items }) {
  return (
    <section className="card p-5">
      <h2 className="text-base font-semibold text-zinc-950">Safe Apply Checklist</h2>
      <div className="mt-4 grid grid-cols-1 gap-2 sm:grid-cols-2">
        {items.map((item) => {
          const Icon = statusIcons[item.status] || CircleHelp;
          return (
            <div key={item.item} className={`flex items-start gap-2 rounded-lg border p-3 text-sm ${statusStyles[item.status]}`}>
              <Icon className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
              <span>{item.item}</span>
            </div>
          );
        })}
      </div>
    </section>
  );
}
