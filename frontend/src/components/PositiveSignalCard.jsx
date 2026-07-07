import { BadgeCheck } from 'lucide-react';

export default function PositiveSignalCard({ items }) {
  return (
    <section className="card p-5">
      <div className="flex items-center gap-2">
        <BadgeCheck className="h-5 w-5 text-emerald-600" aria-hidden="true" />
        <h2 className="text-base font-semibold text-zinc-950">Positive Signals</h2>
      </div>
      <div className="mt-4 grid gap-2">
        {items.map((item) => (
          <div key={item} className="rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-800">
            {item}
          </div>
        ))}
      </div>
    </section>
  );
}
