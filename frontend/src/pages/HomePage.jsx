import { ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

import FeatureCard from '../components/FeatureCard.jsx';
import HeroSection from '../components/HeroSection.jsx';
import ProblemSection from '../components/ProblemSection.jsx';
import { features, scannerSteps } from '../data/content.js';

export default function HomePage() {
  return (
    <>
      <HeroSection />
      <ProblemSection />

      <section className="bg-zinc-50 py-12">
        <div className="page-shell">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div className="max-w-2xl">
              <h2 className="section-title">Cara kerja singkat</h2>
              <p className="mt-3 text-sm leading-6 text-zinc-600">
                LokerLens dibuat untuk keputusan cepat: paste teks, baca sinyal risiko, lalu klarifikasi bagian yang belum jelas.
              </p>
            </div>
            <Link to="/scanner" className="btn-primary w-full sm:w-auto">
              Mulai Scan
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
          </div>

          <div className="mt-6 grid gap-3 md:grid-cols-3">
            {scannerSteps.slice(0, 3).map((step, index) => (
              <article key={step.title} className="rounded-lg border border-zinc-200 bg-white p-4">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-navy-50 text-navy-800">
                  <step.icon className="h-4 w-4" aria-hidden="true" />
                </div>
                <p className="mt-4 text-xs font-semibold uppercase tracking-wide text-zinc-500">Langkah {index + 1}</p>
                <h3 className="mt-1 text-base font-semibold text-zinc-950">{step.title}</h3>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-white py-12">
        <div className="page-shell">
          <div className="max-w-2xl">
            <h2 className="section-title">Fitur utama</h2>
            <p className="mt-3 text-sm leading-6 text-zinc-600">
              Hasil scan dibuat ringkas agar mudah dipakai sebelum mengirim CV atau data pribadi.
            </p>
          </div>
          <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {features.map((feature) => (
              <FeatureCard key={feature.title} {...feature} />
            ))}
          </div>
        </div>
      </section>

      <section className="bg-zinc-50 py-10">
        <div className="page-shell">
          <div className="rounded-lg border border-zinc-200 bg-white p-5 sm:flex sm:items-center sm:justify-between sm:gap-6">
            <p className="text-sm leading-6 text-zinc-700">
              <strong className="text-zinc-950">Catatan:</strong> LokerLens membaca indikasi risiko dari teks lowongan. Keputusan akhir tetap perlu verifikasi kanal resmi dan komunikasi tertulis.
            </p>
            <Link to="/safety-guide" className="btn-secondary mt-4 w-full sm:mt-0 sm:w-auto">
              Panduan Aman Apply
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
