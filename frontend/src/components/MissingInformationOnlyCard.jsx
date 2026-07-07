import { FileWarning } from 'lucide-react';

function normalizeMissingItem(item) {
  if (typeof item === 'string') {
    return {
      field: item.split('.')[0],
      reason: item,
      question: 'Klarifikasi detail ini sebelum apply.',
    };
  }

  return {
    field: item?.field || 'Informasi',
    reason: item?.reason || 'Informasi ini belum disebutkan.',
    question: item?.question || 'Klarifikasi detail ini sebelum apply.',
  };
}

export default function MissingInformationOnlyCard({ items = [] }) {
  const missingItems = items.map(normalizeMissingItem);

  return (
    <section className="card p-5">
      <div className="flex items-start gap-3">
        <FileWarning className="mt-0.5 h-5 w-5 shrink-0 text-amber-600" aria-hidden="true" />
        <div>
          <h2 className="text-base font-semibold text-zinc-950">Informasi yang Belum Disebutkan</h2>
          <p className="mt-1 text-sm leading-6 text-zinc-600">
            Hanya menampilkan bagian penting yang belum jelas dari lowongan.
          </p>
        </div>
      </div>

      <div className="mt-4 grid gap-2">
        {missingItems.length === 0 ? (
          <p className="rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-800">
            Informasi utama pada lowongan ini sudah cukup lengkap.
          </p>
        ) : (
          missingItems.map((item, index) => (
            <article key={`${item.field}-${index}`} className="rounded-lg border border-amber-200 bg-amber-50 p-3">
              <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                <h3 className="text-sm font-semibold text-amber-950">{item.field} tidak disebutkan</h3>
                <span className="w-fit rounded-full border border-amber-300 bg-white px-2 py-0.5 text-[11px] font-semibold text-amber-800">
                  missing
                </span>
              </div>
              <p className="mt-2 text-sm leading-6 text-amber-900">{item.reason}</p>
              <p className="mt-2 text-sm font-medium leading-6 text-amber-950">{item.question}</p>
            </article>
          ))
        )}
      </div>
    </section>
  );
}
