import { BriefcaseBusiness } from 'lucide-react';

const labels = [
  ['position', 'Posisi'],
  ['company', 'Perusahaan'],
  ['job_type', 'Jenis lowongan'],
  ['source_platform', 'Platform sumber'],
  ['compensation', 'Kompensasi'],
  ['working_hours', 'Jam kerja'],
  ['workload', 'Workload'],
  ['benefits', 'Benefit'],
  ['contact', 'Kontak'],
  ['notes', 'Catatan penting'],
];

export default function JobSummaryCard({ summary }) {
  if (!summary) return null;

  return (
    <section className="card p-5">
      <div className="flex items-center gap-2">
        <BriefcaseBusiness className="h-5 w-5 text-navy-800" aria-hidden="true" />
        <h2 className="text-base font-semibold text-zinc-950">Lowongan Summary</h2>
      </div>
      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        {labels.map(([key, label]) => (
          <div key={key} className="rounded-lg border border-zinc-200 bg-zinc-50 p-3">
            <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">{label}</p>
            <p className="mt-1 text-sm leading-6 text-zinc-800">{summary[key] || 'Belum disebutkan'}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
