import { SearchCheck } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function EmptyHistoryState({ compact = false }) {
  return (
    <section className={`card text-center ${compact ? 'p-5' : 'p-8'}`}>
      <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-lg bg-navy-50 text-navy-800">
        <SearchCheck className="h-6 w-6" aria-hidden="true" />
      </div>
      <h2 className="mt-5 text-lg font-semibold text-zinc-950">Belum ada riwayat scan.</h2>
      <p className="mt-2 text-sm leading-6 text-zinc-600">
        Mulai scan lowongan untuk menyimpan hasil analisis ke akun kamu.
      </p>
      {!compact && (
        <Link to="/scanner" className="btn-primary mt-5">
          Scan Lowongan
        </Link>
      )}
    </section>
  );
}
