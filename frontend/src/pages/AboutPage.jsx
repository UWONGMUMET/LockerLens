import { UsersRound } from 'lucide-react';

export default function AboutPage() {
  return (
    <section className="bg-white py-12">
      <div className="page-shell grid gap-8 lg:grid-cols-[0.8fr_1.2fr] lg:items-start">
        <div className="rounded-lg border border-zinc-200 bg-zinc-50 p-6">
          <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-navy-800 text-white">
            <UsersRound className="h-6 w-6" aria-hidden="true" />
          </div>
          <h1 className="mt-5 text-3xl font-semibold tracking-normal text-zinc-950">Tentang LokerLens</h1>
          <p className="mt-4 text-sm leading-6 text-zinc-600">
            Dibuat untuk membantu pencari kerja pemula membaca lowongan digital dengan lebih kritis dan tenang.
          </p>
        </div>

        <div className="space-y-4 text-base leading-7 text-zinc-700">
          <p>
            LokerLens dibuat untuk membantu mahasiswa dan pencari kerja pemula lebih kritis saat membaca lowongan digital.
          </p>
          <p>
            Banyak lowongan tersebar di media sosial dan grup komunitas. Formatnya cepat dibagikan, tetapi sering tidak memuat detail yang cukup tentang kompensasi, jam kerja, kontrak, supervisor, atau kanal resmi perusahaan.
          </p>
          <p>
            Hasil scan LokerLens adalah rekomendasi awal. Keputusan akhir tetap membutuhkan penilaian manusia, verifikasi kanal resmi, dan komunikasi tertulis yang jelas dengan recruiter atau perusahaan.
          </p>
        </div>
      </div>
    </section>
  );
}
