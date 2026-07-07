import { ClipboardList } from 'lucide-react';

function fallbackSummary(items = []) {
  if (items.length === 0) {
    return 'Informasi utama pada lowongan ini sudah cukup lengkap. Tetap cocokkan sumber lowongan dengan kanal resmi sebelum apply.';
  }

  if (items.length <= 2) {
    return 'Sebagian besar informasi utama sudah tersedia. Namun, user tetap perlu mengklarifikasi bagian yang belum disebutkan sebelum apply.';
  }

  return 'Lowongan ini masih memiliki banyak informasi penting yang belum disebutkan. Sebaiknya lakukan klarifikasi terlebih dahulu sebelum mengirim CV atau data pribadi.';
}

export default function MissingInfoSummaryCard({ summary, items = [] }) {
  return (
    <section className="rounded-lg border border-zinc-200 bg-zinc-50 p-5">
      <div className="flex items-center gap-2">
        <ClipboardList className="h-5 w-5 text-navy-800" aria-hidden="true" />
        <h2 className="text-base font-semibold text-zinc-950">Ringkasan Missing Info</h2>
      </div>
      <p className="mt-3 text-sm leading-6 text-zinc-700">{summary || fallbackSummary(items)}</p>
    </section>
  );
}
