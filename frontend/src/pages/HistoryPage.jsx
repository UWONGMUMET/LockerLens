import { History } from 'lucide-react';
import { useState } from 'react';

import HistoryDrawer from '../components/HistoryDrawer.jsx';

export default function HistoryPage() {
  const [open, setOpen] = useState(true);

  return (
    <section className="bg-zinc-50 py-12">
      <div className="page-shell">
        <div className="card mx-auto max-w-xl p-6 text-center">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-lg bg-navy-50 text-navy-800">
            <History className="h-6 w-6" aria-hidden="true" />
          </div>
          <h1 className="mt-5 text-2xl font-semibold tracking-normal text-zinc-950">Riwayat scan ada di drawer.</h1>
          <p className="mt-2 text-sm leading-6 text-zinc-600">
            Buka panel riwayat untuk melihat list scan, membaca detail, menghapus item, atau scan ulang teks lama.
          </p>
          <button type="button" className="btn-primary mt-5" onClick={() => setOpen(true)}>
            Buka Riwayat Scan
          </button>
        </div>
      </div>

      <HistoryDrawer open={open} onOpenChange={setOpen} />
    </section>
  );
}
