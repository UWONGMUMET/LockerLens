import { FileWarning } from 'lucide-react';

export default function MissingInfoCard({ items }) {
  return (
    <section className="card p-5">
      <div className="flex items-center gap-2">
        <FileWarning className="h-5 w-5 text-amber-600" aria-hidden="true" />
        <h2 className="text-base font-semibold text-zinc-950">Missing Information</h2>
      </div>
      <div className="mt-4 grid gap-2">
        {items.length === 0 ? (
          <p className="text-sm text-zinc-600">Informasi inti terlihat cukup lengkap.</p>
        ) : (
          items.map((item) => (
            <div key={item} className="rounded-lg border border-zinc-200 bg-zinc-50 p-3 text-sm text-zinc-700">
              {item}
            </div>
          ))
        )}
      </div>
    </section>
  );
}
