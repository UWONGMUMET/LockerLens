import { ShieldAlert } from 'lucide-react';

export default function PersonalDataWarningCard({ warning }) {
  if (!warning?.is_detected) return null;

  return (
    <section className="rounded-lg border border-red-200 bg-red-50 p-5">
      <div className="flex items-start gap-3">
        <ShieldAlert className="mt-0.5 h-5 w-5 shrink-0 text-red-700" aria-hidden="true" />
        <div>
          <h2 className="text-base font-semibold text-red-900">Personal Data Warning</h2>
          <p className="mt-2 text-sm leading-6 text-red-800">{warning.message}</p>
          <div className="mt-3 flex flex-wrap gap-2">
            {warning.detected_terms.map((term) => (
              <span key={term} className="rounded-full border border-red-200 bg-white px-2 py-1 text-xs font-semibold text-red-700">
                {term}
              </span>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
