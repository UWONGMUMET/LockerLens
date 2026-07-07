import { ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

import RiskBadge from './RiskBadge.jsx';

export default function HeroSection() {
  return (
    <section className="relative isolate overflow-hidden bg-navy-900 text-white">
      <div className="page-shell relative grid min-h-[64vh] gap-8 py-14 lg:grid-cols-[0.95fr_1.05fr] lg:items-center">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wide text-navy-100">LokerLens</p>
          <h1 className="mt-4 max-w-2xl text-4xl font-semibold tracking-normal text-white sm:text-5xl">
            Scan lowongan sebelum kamu apply.
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-7 text-zinc-200 sm:text-lg">
            LokerLens membantu kamu membaca risiko lowongan magang, freelance, dan part-time dari teks lowongan digital.
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link to="/scanner" className="btn-primary bg-white text-navy-900 hover:bg-zinc-100">
              Scan Lowongan
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
            <Link to="/safety-guide" className="btn-secondary border-white/30 bg-transparent text-white hover:border-white hover:text-white">
              Lihat Panduan Aman Apply
            </Link>
          </div>
        </div>

        <div className="rounded-lg border border-white/15 bg-white/10 p-4 backdrop-blur">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <span className="text-sm font-semibold text-white">Preview Hasil Scan</span>
            <RiskBadge score={72} label="Cukup Aman, Tapi Perlu Dicek" />
          </div>
          <div className="mt-5 grid gap-3 sm:grid-cols-3">
            <div className="rounded-lg bg-white p-4 text-zinc-950">
              <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">Trust Score</p>
              <p className="mt-3 text-4xl font-semibold">72</p>
            </div>
            <div className="rounded-lg bg-white p-4 text-zinc-950">
              <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">Red Flag</p>
              <p className="mt-3 text-sm leading-6">Kompensasi perlu dikonfirmasi tertulis.</p>
            </div>
            <div className="rounded-lg bg-white p-4 text-zinc-950">
              <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">Action</p>
              <p className="mt-3 text-sm leading-6">Tanyakan detail kerja sebelum lanjut.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
