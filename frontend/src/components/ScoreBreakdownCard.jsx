import { ListMinus } from 'lucide-react';

export default function ScoreBreakdownCard({ items }) {
  return (
    <section className="card p-5">
      <div className="flex items-center gap-2">
        <ListMinus className="h-5 w-5 text-navy-800" aria-hidden="true" />
        <h2 className="text-base font-semibold text-zinc-950">Trust Score Breakdown</h2>
      </div>
      <div className="mt-4 grid gap-3">
        {items.length === 0 ? (
          <p className="rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-800">
            Tidak ada pengurangan skor utama yang terbaca.
          </p>
        ) : (
          items.map((item, index) => (
            <div key={`${item.category}-${index}`} className="rounded-lg border border-zinc-200 bg-zinc-50 p-4">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h3 className="text-sm font-semibold text-zinc-950">{item.category}</h3>
                  <p className="mt-1 text-sm leading-6 text-zinc-600">{item.evidence}</p>
                </div>
                <span className="rounded-full border border-red-200 bg-red-50 px-2 py-1 text-xs font-semibold text-red-700">
                  -{item.deduction}
                </span>
              </div>
              <p className="mt-3 text-sm leading-6 text-zinc-600">{item.explanation}</p>
            </div>
          ))
        )}
      </div>
    </section>
  );
}
