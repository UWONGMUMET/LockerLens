import { ExternalLink, Link2, Tags } from 'lucide-react';

const platformLabels = {
  instagram: 'Instagram',
  linkedin: 'LinkedIn',
  twitter: 'X/Twitter',
  telegram: 'Telegram',
  job_site: 'Website Karier',
  other: 'Lainnya',
};

export default function SourceReferenceCard({ result }) {
  const sourceUrl = result?.source_url;
  const sourceHref = sourceUrl ? (/^https?:\/\//i.test(sourceUrl) ? sourceUrl : `https://${sourceUrl}`) : '';
  const keywords = result?.keywords_checked || [];

  if (!sourceUrl && keywords.length === 0) return null;

  return (
    <section className="card p-5">
      <div className="flex items-center gap-2">
        <Link2 className="h-5 w-5 text-navy-800" aria-hidden="true" />
        <h2 className="text-base font-semibold text-zinc-950">Referensi Sumber</h2>
      </div>

      <div className="mt-4 grid gap-4 text-sm">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">Platform</p>
          <p className="mt-1 font-medium text-zinc-800">
            {platformLabels[result?.source_platform] || result?.source_platform || 'Tidak disebutkan'}
          </p>
        </div>

        {sourceUrl && (
          <a
            href={sourceHref}
            target="_blank"
            rel="noreferrer"
            className="inline-flex w-fit items-center gap-2 rounded-lg border border-zinc-300 bg-white px-3 py-2 text-sm font-semibold text-zinc-900 transition hover:border-navy-700 hover:text-navy-800"
          >
            <ExternalLink className="h-4 w-4" aria-hidden="true" />
            Buka Sumber Lowongan
          </a>
        )}

        {keywords.length > 0 && (
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-zinc-500">
              <Tags className="h-3.5 w-3.5" aria-hidden="true" />
              Kata kunci yang diperiksa
            </div>
            <div className="mt-2 flex flex-wrap gap-2">
              {keywords.map((keyword) => (
                <span key={keyword} className="rounded-full border border-navy-100 bg-navy-50 px-2.5 py-1 text-xs font-semibold text-navy-800">
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
