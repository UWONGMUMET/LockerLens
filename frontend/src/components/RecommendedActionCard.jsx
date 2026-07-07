import { ClipboardCheck } from 'lucide-react';

export default function RecommendedActionCard({ action, note }) {
  return (
    <section className="card p-5">
      <div className="flex items-center gap-2">
        <ClipboardCheck className="h-5 w-5 text-navy-800" aria-hidden="true" />
        <h2 className="text-base font-semibold text-zinc-950">Recommended Action</h2>
      </div>
      <p className="mt-4 text-sm leading-6 text-zinc-700">{action}</p>
      <div className="mt-4 rounded-lg border border-zinc-200 bg-zinc-50 p-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">Safety Note</p>
        <p className="mt-2 text-sm leading-6 text-zinc-700">{note}</p>
      </div>
    </section>
  );
}
