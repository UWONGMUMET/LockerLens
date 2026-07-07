import { Eye, Trash2 } from 'lucide-react';

import RiskBadge from './RiskBadge.jsx';

const jobTypeLabels = {
  internship: 'Magang',
  freelance: 'Freelance',
  part_time: 'Part-time',
  entry_level: 'Entry-level',
};

const platformLabels = {
  instagram: 'Instagram',
  linkedin: 'LinkedIn',
  twitter: 'X/Twitter',
  telegram: 'Telegram',
  job_site: 'Website Karier',
  other: 'Lainnya',
};

export default function HistoryListItem({ item, selected, onSelect, onDelete, deleting }) {
  return (
    <article
      className={[
        'rounded-lg border bg-white p-3 shadow-soft transition',
        selected ? 'border-navy-700' : 'border-zinc-200 hover:border-zinc-300',
      ].join(' ')}
    >
      <div className="w-full text-left">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <span className="rounded-lg bg-zinc-950 px-2 py-1 text-xs font-semibold text-white">
                {item.trust_score}
              </span>
              <RiskBadge score={item.trust_score} label={item.risk_level} />
            </div>
            <p className="mt-2 text-xs font-semibold uppercase tracking-wide text-zinc-500">
              {jobTypeLabels[item.job_type] || item.job_type} / {platformLabels[item.source_platform] || item.source_platform}
            </p>
          </div>
          <Eye className="mt-1 h-4 w-4 shrink-0 text-zinc-400" aria-hidden="true" />
        </div>

        <p
          className="mt-3 text-sm leading-6 text-zinc-700"
          style={{
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
          }}
        >
          {item.job_preview}
        </p>
        <p className="mt-2 text-xs text-zinc-500">{new Date(item.created_at).toLocaleString('id-ID')}</p>
        <p className="mt-2 truncate rounded-lg border border-zinc-200 bg-zinc-50 px-3 py-2 text-xs font-medium text-zinc-700">
          {item.recommended_action}
        </p>
      </div>

      <div className="mt-3 grid grid-cols-2 gap-2">
        <button type="button" className="btn-secondary px-3 py-2" onClick={() => onSelect(item.id)}>
          <Eye className="h-4 w-4" aria-hidden="true" />
          Lihat Detail
        </button>
        <button
          type="button"
          className="inline-flex items-center justify-center gap-2 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm font-semibold text-red-700 transition hover:bg-red-100 disabled:opacity-60"
          onClick={() => onDelete(item.id)}
          disabled={deleting}
        >
          <Trash2 className="h-4 w-4" aria-hidden="true" />
          Hapus
        </button>
      </div>
    </article>
  );
}
