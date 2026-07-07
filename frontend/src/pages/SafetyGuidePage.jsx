import * as Accordion from '@radix-ui/react-accordion';
import { ChevronDown } from 'lucide-react';

import SafetyChecklist from '../components/SafetyChecklist.jsx';
import {
  recruiterQuestions,
  redFlagExamples,
  sensitiveData,
  verificationTips,
} from '../data/content.js';

function GuidePanel({ value, title, items, tone = 'default' }) {
  const toneClass =
    tone === 'danger'
      ? 'border-red-200 bg-red-50 text-red-800'
      : tone === 'warning'
        ? 'border-amber-200 bg-amber-50 text-amber-800'
        : 'border-zinc-200 bg-white text-zinc-700';

  return (
    <Accordion.Item value={value} className={`rounded-lg border ${toneClass}`}>
      <Accordion.Trigger className="group flex w-full items-center justify-between gap-4 px-4 py-3 text-left">
        <span className="text-base font-semibold">{title}</span>
        <ChevronDown className="h-4 w-4 shrink-0 transition group-data-[state=open]:rotate-180" aria-hidden="true" />
      </Accordion.Trigger>
      <Accordion.Content className="px-4 pb-4">
        <ul className="grid gap-2 text-sm leading-6">
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </Accordion.Content>
    </Accordion.Item>
  );
}

export default function SafetyGuidePage() {
  return (
    <section className="bg-zinc-50 py-12">
      <div className="page-shell">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-wide text-navy-800">Safety Guide</p>
          <h1 className="mt-3 text-3xl font-semibold tracking-normal text-zinc-950 sm:text-4xl">
            Panduan cepat sebelum apply lowongan digital.
          </h1>
          <p className="mt-4 text-base leading-7 text-zinc-600">
            Buka bagian yang kamu perlukan, lalu cocokkan dengan teks lowongan yang sedang dibaca.
          </p>
        </div>

        <div className="mt-8 grid gap-5 lg:grid-cols-[0.95fr_1.05fr] lg:items-start">
          <section className="card p-5">
            <h2 className="text-xl font-semibold text-zinc-950">Checklist sebelum apply</h2>
            <div className="mt-4">
              <SafetyChecklist />
            </div>
          </section>

          <Accordion.Root type="multiple" defaultValue={['sensitive-data']} className="grid gap-3">
            <GuidePanel
              value="sensitive-data"
              title="Data pribadi yang tidak boleh diberikan terlalu awal"
              items={sensitiveData}
              tone="danger"
            />
            <GuidePanel
              value="questions"
              title="Pertanyaan yang perlu ditanyakan ke recruiter"
              items={recruiterQuestions}
            />
            <GuidePanel
              value="red-flags"
              title="Contoh red flag lowongan"
              items={redFlagExamples}
              tone="warning"
            />
            <GuidePanel
              value="verification"
              title="Tips verifikasi perusahaan"
              items={verificationTips}
            />
          </Accordion.Root>
        </div>
      </div>
    </section>
  );
}
