import * as Accordion from '@radix-ui/react-accordion';
import { AlertTriangle, ChevronDown } from 'lucide-react';

const severityStyles = {
  low: 'border-amber-200 bg-amber-50 text-amber-700',
  medium: 'border-orange-200 bg-orange-50 text-orange-700',
  high: 'border-red-200 bg-red-50 text-red-700',
};

export default function RedFlagAccordion({ flags }) {
  return (
    <section className="card p-5">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-semibold text-zinc-950">Red Flags</h2>
          <p className="mt-1 text-sm text-zinc-600">Indikasi risiko yang perlu diverifikasi.</p>
        </div>
        <AlertTriangle className="h-5 w-5 text-orange-500" aria-hidden="true" />
      </div>

      {flags.length === 0 ? (
        <p className="mt-5 rounded-lg border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-800">
          Tidak ada red flag kuat yang terbaca dari teks ini.
        </p>
      ) : (
        <Accordion.Root type="single" collapsible className="mt-4 divide-y divide-zinc-200">
          {flags.map((flag, index) => (
            <Accordion.Item key={`${flag.category}-${index}`} value={`flag-${index}`}>
              <Accordion.Trigger className="group flex w-full items-center justify-between gap-4 py-4 text-left">
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-sm font-semibold text-zinc-950">{flag.category}</span>
                    <span className={`rounded-full border px-2 py-0.5 text-[11px] font-semibold ${severityStyles[flag.severity]}`}>
                      {flag.severity}
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-zinc-500">Pengurangan skor: {flag.deduction}</p>
                </div>
                <ChevronDown className="h-4 w-4 shrink-0 text-zinc-500 transition group-data-[state=open]:rotate-180" />
              </Accordion.Trigger>
              <Accordion.Content className="pb-4 text-sm leading-6 text-zinc-600">
                <p className="rounded-lg bg-zinc-50 p-3 text-zinc-700">{flag.evidence}</p>
                <p className="mt-3">{flag.explanation}</p>
              </Accordion.Content>
            </Accordion.Item>
          ))}
        </Accordion.Root>
      )}
    </section>
  );
}
