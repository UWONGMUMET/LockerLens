import { ArrowLeft, RotateCcw, Trash2 } from 'lucide-react';

import ScanResultSections from './ScanResultSections.jsx';

export default function HistoryDetail({ detail, loading, deleting, onBack, onDelete, onReuse }) {
  if (loading) {
    return <div className="card p-5 text-sm text-zinc-600">Memuat detail...</div>;
  }

  if (!detail) {
    return (
      <section className="card flex min-h-[220px] items-center justify-center p-6 text-center">
        <div>
          <h2 className="text-base font-semibold text-zinc-950">Pilih riwayat scan.</h2>
          <p className="mt-2 text-sm leading-6 text-zinc-600">Detail hasil scan akan tampil di sini.</p>
        </div>
      </section>
    );
  }

  return (
    <div className="space-y-4">
      <section className="card p-4">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <button type="button" className="btn-secondary mb-3" onClick={onBack}>
              <ArrowLeft className="h-4 w-4" aria-hidden="true" />
              Kembali
            </button>
            <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">Detail riwayat</p>
            <h2 className="mt-1 text-lg font-semibold text-zinc-950">
              Scan #{detail.id} / {new Date(detail.created_at).toLocaleString('id-ID')}
            </h2>
          </div>
          <div className="flex flex-col gap-2 sm:flex-row">
            <button type="button" className="btn-secondary" onClick={() => onReuse(detail)}>
              <RotateCcw className="h-4 w-4" aria-hidden="true" />
              Scan ulang teks ini
            </button>
            <button
              type="button"
              className="inline-flex items-center justify-center gap-2 rounded-lg border border-red-200 bg-red-50 px-4 py-2.5 text-sm font-semibold text-red-700 transition hover:bg-red-100 disabled:opacity-60"
              onClick={() => onDelete(detail.id)}
              disabled={deleting}
            >
              <Trash2 className="h-4 w-4" aria-hidden="true" />
              Hapus
            </button>
          </div>
        </div>
      </section>

      <ScanResultSections result={detail} compact />
    </div>
  );
}
