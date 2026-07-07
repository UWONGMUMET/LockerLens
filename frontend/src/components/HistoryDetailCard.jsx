import ScanResultSections from './ScanResultSections.jsx';

export default function HistoryDetailCard({ detail }) {
  if (!detail) {
    return (
      <section className="card flex min-h-[240px] items-center justify-center p-6 text-center">
        <div>
          <h2 className="text-base font-semibold text-zinc-950">Pilih riwayat scan.</h2>
          <p className="mt-2 text-sm leading-6 text-zinc-600">Detail hasil scan akan tampil di sini.</p>
        </div>
      </section>
    );
  }

  return (
    <div className="space-y-5">
      <section className="card p-5">
        <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">History detail</p>
        <h2 className="mt-2 text-lg font-semibold text-zinc-950">
          Scan #{detail.id} · {new Date(detail.created_at).toLocaleString('id-ID')}
        </h2>
      </section>
      <ScanResultSections result={detail} jobText={detail.job_text} />
    </div>
  );
}
