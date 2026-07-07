import { problemItems } from '../data/content.js';

export default function ProblemSection() {
  return (
    <section className="border-b border-zinc-200 bg-white py-12">
      <div className="page-shell">
        <div className="max-w-3xl">
          <h2 className="section-title">Lowongan digital sering kurang transparan.</h2>
          <p className="mt-4 text-base leading-7 text-zinc-600">
            Mahasiswa, fresh graduate, dan freelancer pemula sering menemukan lowongan dari media sosial atau grup komunitas. Banyak yang valid, tetapi sebagian perlu dibaca lebih kritis sebelum apply.
          </p>
        </div>
        <div className="mt-8 grid gap-3 md:grid-cols-2">
          {problemItems.map((item) => (
            <div key={item} className="rounded-lg border border-zinc-200 bg-zinc-50 p-4 text-sm leading-6 text-zinc-700">
              {item}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
