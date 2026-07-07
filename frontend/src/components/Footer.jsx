import { SearchCheck } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="border-t border-zinc-200 bg-zinc-50">
      <div className="page-shell grid gap-8 py-10 md:grid-cols-[1.3fr_1fr_1fr]">
        <div>
          <div className="flex items-center gap-2 text-lg font-semibold text-zinc-950">
            <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-navy-800 text-white">
              <SearchCheck className="h-5 w-5" aria-hidden="true" />
            </span>
            <span>LokerLens</span>
          </div>
          <p className="mt-4 max-w-md text-sm leading-6 text-zinc-600">
            Membantu mahasiswa, fresh graduate, dan freelancer pemula membaca indikasi risiko lowongan digital sebelum apply.
          </p>
        </div>
        <div>
          <h2 className="text-sm font-semibold text-zinc-950">Navigasi</h2>
          <div className="mt-3 grid gap-2 text-sm text-zinc-600">
            <Link to="/scanner" className="hover:text-navy-800">Scanner</Link>
            <Link to="/safety-guide" className="hover:text-navy-800">Safety Guide</Link>
            <Link to="/about" className="hover:text-navy-800">About</Link>
          </div>
        </div>
        <div>
          <h2 className="text-sm font-semibold text-zinc-950">Catatan</h2>
          <p className="mt-3 text-sm leading-6 text-zinc-600">
            Hasil scan adalah rekomendasi awal. Tetap verifikasi kanal resmi dan gunakan penilaian manusia sebelum mengambil keputusan.
          </p>
        </div>
      </div>
    </footer>
  );
}
