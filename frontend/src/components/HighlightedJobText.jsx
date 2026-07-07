import { Highlighter } from 'lucide-react';

const highlightStyles = {
  high: 'bg-red-100 text-red-900 ring-red-200',
  medium: 'bg-amber-100 text-amber-900 ring-amber-200',
  low: 'bg-yellow-100 text-yellow-900 ring-yellow-200',
};

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function buildSegments(text, terms) {
  const realTerms = terms
    .filter((item) => item.term && text.toLowerCase().includes(item.term.toLowerCase()))
    .sort((a, b) => b.term.length - a.term.length);

  if (realTerms.length === 0) return [{ text, match: null }];

  const pattern = new RegExp(`(${realTerms.map((item) => escapeRegExp(item.term)).join('|')})`, 'gi');
  const chunks = text.split(pattern).filter(Boolean);
  return chunks.map((chunk) => {
    const match = realTerms.find((item) => item.term.toLowerCase() === chunk.toLowerCase());
    return { text: chunk, match };
  });
}

export default function HighlightedJobText({ text, terms }) {
  const segments = buildSegments(text || '', terms || []);
  const unmatchedTerms = (terms || []).filter((item) => item.term && !(text || '').toLowerCase().includes(item.term.toLowerCase()));

  return (
    <section className="card p-5">
      <div className="flex items-center gap-2">
        <Highlighter className="h-5 w-5 text-navy-800" aria-hidden="true" />
        <h2 className="text-base font-semibold text-zinc-950">Risk Highlight</h2>
      </div>
      <div className="mt-4 max-h-[360px] overflow-auto rounded-lg border border-zinc-200 bg-zinc-50 p-4 text-sm leading-7 text-zinc-800">
        {segments.map((segment, index) =>
          segment.match ? (
            <mark
              key={`${segment.text}-${index}`}
              className={`rounded px-1 py-0.5 ring-1 ${highlightStyles[segment.match.severity]}`}
              title={segment.match.explanation}
            >
              {segment.text}
            </mark>
          ) : (
            <span key={`${segment.text}-${index}`}>{segment.text}</span>
          ),
        )}
      </div>
      {unmatchedTerms.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-2">
          {unmatchedTerms.map((item) => (
            <span key={`${item.term}-${item.category}`} className={`rounded-full px-2 py-1 text-xs font-semibold ring-1 ${highlightStyles[item.severity]}`}>
              {item.term}
            </span>
          ))}
        </div>
      )}
    </section>
  );
}
