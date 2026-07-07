import { MessageCircleQuestion } from 'lucide-react';

export default function QuestionsToAskCard({ items = [] }) {
  return (
    <section className="card p-5">
      <div className="flex items-center gap-2">
        <MessageCircleQuestion className="h-5 w-5 text-navy-800" aria-hidden="true" />
        <h2 className="text-base font-semibold text-zinc-950">Questions to Ask</h2>
      </div>
      {items.length === 0 ? (
        <p className="mt-4 rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-800">
          Belum ada pertanyaan klarifikasi utama dari hasil scan ini.
        </p>
      ) : (
        <ol className="mt-4 grid gap-3">
          {items.map((item, index) => (
            <li key={item} className="flex gap-3 text-sm leading-6 text-zinc-700">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-navy-50 text-xs font-semibold text-navy-800">
                {index + 1}
              </span>
              <span>{item}</span>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
