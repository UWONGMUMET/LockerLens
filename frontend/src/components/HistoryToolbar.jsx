import { RefreshCw, X } from 'lucide-react';

export default function HistoryToolbar({ count, loading, onRefresh, onClose }) {
  return (
    <div className="flex items-center justify-between gap-3 border-b border-zinc-200 px-4 py-3">
      <div>
        <h2 className="text-base font-semibold text-zinc-950">Riwayat Scan</h2>
        <p className="text-xs text-zinc-500">{loading ? 'Memuat riwayat...' : `${count} hasil scan tersimpan`}</p>
      </div>
      <div className="flex items-center gap-2">
        <button
          type="button"
          className="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-zinc-200 text-zinc-700 transition hover:border-navy-700 hover:text-navy-800"
          onClick={onRefresh}
          disabled={loading}
          aria-label="Muat ulang riwayat"
        >
          <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} aria-hidden="true" />
        </button>
        <button
          type="button"
          className="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-zinc-200 text-zinc-700 transition hover:border-navy-700 hover:text-navy-800"
          onClick={onClose}
          aria-label="Tutup riwayat"
        >
          <X className="h-4 w-4" aria-hidden="true" />
        </button>
      </div>
    </div>
  );
}
