import { ArrowRight, ClipboardPaste, History, Loader2, RotateCcw, X } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';

import { useAuth } from '../context/AuthContext.jsx';
import { sampleJobText } from '../data/content.js';
import { scanJob } from '../lib/api.js';
import HistoryDrawer from './HistoryDrawer.jsx';
import ScanResultSections from './ScanResultSections.jsx';

const jobTypes = [
  { value: 'internship', label: 'Magang' },
  { value: 'freelance', label: 'Freelance' },
  { value: 'part_time', label: 'Part-time' },
  { value: 'entry_level', label: 'Entry-level' },
];

const platforms = [
  { value: 'instagram', label: 'Instagram' },
  { value: 'linkedin', label: 'LinkedIn' },
  { value: 'twitter', label: 'X/Twitter' },
  { value: 'telegram', label: 'Telegram' },
  { value: 'job_site', label: 'Website Karier' },
  { value: 'other', label: 'Lainnya' },
];

function splitKeywords(value) {
  return value
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
}

function mergeKeywords(current, draft = '') {
  const seen = new Set();
  return [...current, ...splitKeywords(draft)]
    .map((item) => item.trim())
    .filter(Boolean)
    .filter((item) => {
      const key = item.toLowerCase();
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    })
    .slice(0, 20);
}

export default function ScannerForm() {
  const { isAuthenticated } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [jobText, setJobText] = useState('');
  const [jobType, setJobType] = useState('internship');
  const [sourcePlatform, setSourcePlatform] = useState('instagram');
  const [sourceUrl, setSourceUrl] = useState('');
  const [keywords, setKeywords] = useState([]);
  const [keywordDraft, setKeywordDraft] = useState('');
  const [historyOpen, setHistoryOpen] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const reuseScan = location.state?.reuseScan;
    if (!reuseScan) return;

    setJobText(reuseScan.job_text || '');
    setJobType(reuseScan.job_type || 'internship');
    setSourcePlatform(reuseScan.source_platform || 'instagram');
    setSourceUrl(reuseScan.source_url || '');
    setKeywords(reuseScan.keywords_checked || []);
    setKeywordDraft('');
    setResult(null);
    setError('');
    navigate(location.pathname, { replace: true });
  }, [location.pathname, location.state, navigate]);

  function addKeywords(value = keywordDraft) {
    setKeywords((current) => mergeKeywords(current, value));
    setKeywordDraft('');
  }

  function removeKeyword(keyword) {
    setKeywords((current) => current.filter((item) => item !== keyword));
  }

  function handleKeywordKeyDown(event) {
    if (event.key !== 'Enter' && event.key !== ',') return;
    event.preventDefault();
    addKeywords();
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');

    if (jobText.trim().length < 20) {
      setError('Paste teks lowongan yang lebih lengkap untuk dianalisis.');
      return;
    }

    const keywordsForRequest = mergeKeywords(keywords, keywordDraft);
    const cleanedSourceUrl = sourceUrl.trim() || null;
    setKeywords(keywordsForRequest);
    setKeywordDraft('');
    setLoading(true);

    try {
      const data = await scanJob({
        job_text: jobText,
        job_type: jobType,
        source_platform: sourcePlatform,
        source_url: cleanedSourceUrl,
        keywords: keywordsForRequest,
      });
      setResult({
        ...data,
        job_type: data.job_type || jobType,
        source_platform: data.source_platform || sourcePlatform,
        source_url: data.source_url ?? cleanedSourceUrl,
        keywords_checked: data.keywords_checked?.length ? data.keywords_checked : keywordsForRequest,
      });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  function handleReuseScan(detail) {
    setJobText(detail.job_text || '');
    setJobType(detail.job_type || 'internship');
    setSourcePlatform(detail.source_platform || 'instagram');
    setSourceUrl(detail.source_url || '');
    setKeywords(detail.keywords_checked || []);
    setKeywordDraft('');
    setResult(null);
    setError('');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  return (
    <div className="mx-auto max-w-[1100px] space-y-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-normal text-zinc-950 sm:text-3xl">Scanner Lowongan</h1>
          <p className="mt-1 text-sm leading-6 text-zinc-600">
            Paste teks lowongan, pilih konteks, lalu cek risiko tanpa pindah halaman.
          </p>
        </div>
        {isAuthenticated && (
          <button type="button" className="btn-secondary w-full sm:w-auto" onClick={() => setHistoryOpen(true)}>
            <History className="h-4 w-4" aria-hidden="true" />
            Riwayat
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12 lg:items-start">
        <section className="card p-4 sm:p-5 lg:col-span-8">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-base font-semibold text-zinc-950">Teks dan sumber lowongan</h2>
                <p className="mt-1 text-sm text-zinc-600">Field link dan kata kunci opsional.</p>
              </div>
              <button
                type="button"
                className="btn-secondary w-full sm:w-auto"
                onClick={() => {
                  setJobText(sampleJobText);
                  setSourcePlatform('linkedin');
                  setSourceUrl('https://www.linkedin.com/jobs/view/contoh-lokerlens');
                  setKeywords(['paid', 'hybrid', 'social media']);
                  setKeywordDraft('');
                  setResult(null);
                  setError('');
                }}
              >
                <ClipboardPaste className="h-4 w-4" aria-hidden="true" />
                Gunakan contoh
              </button>
            </div>

            <label className="block">
              <span className="text-sm font-semibold text-zinc-800">Teks Lowongan</span>
              <textarea
                value={jobText}
                onChange={(event) => setJobText(event.target.value)}
                rows={8}
                className="mt-2 min-h-[150px] max-h-[240px] w-full resize-y rounded-lg border border-zinc-300 bg-white p-3 text-sm leading-6 text-zinc-900 outline-none transition placeholder:text-zinc-400 focus:border-navy-700 focus:ring-2 focus:ring-navy-100 sm:min-h-[180px]"
                placeholder="Paste teks lowongan magang, freelance, part-time, atau entry-level di sini..."
              />
            </label>

            <div className="grid gap-3 sm:grid-cols-2">
              <label className="block">
                <span className="text-sm font-semibold text-zinc-800">Jenis lowongan</span>
                <select
                  value={jobType}
                  onChange={(event) => setJobType(event.target.value)}
                  className="mt-2 h-11 w-full rounded-lg border border-zinc-300 bg-white px-3 text-sm text-zinc-900 outline-none focus:border-navy-700 focus:ring-2 focus:ring-navy-100"
                >
                  {jobTypes.map((item) => (
                    <option key={item.value} value={item.value}>{item.label}</option>
                  ))}
                </select>
              </label>
              <label className="block">
                <span className="text-sm font-semibold text-zinc-800">Source Platform</span>
                <select
                  value={sourcePlatform}
                  onChange={(event) => setSourcePlatform(event.target.value)}
                  className="mt-2 h-11 w-full rounded-lg border border-zinc-300 bg-white px-3 text-sm text-zinc-900 outline-none focus:border-navy-700 focus:ring-2 focus:ring-navy-100"
                >
                  {platforms.map((item) => (
                    <option key={item.value} value={item.value}>{item.label}</option>
                  ))}
                </select>
              </label>
            </div>

            <label className="block">
              <span className="text-sm font-semibold text-zinc-800">Link sumber lowongan</span>
              <input
                value={sourceUrl}
                onChange={(event) => setSourceUrl(event.target.value)}
                type="text"
                inputMode="url"
                className="mt-2 h-11 w-full rounded-lg border border-zinc-300 bg-white px-3 text-sm text-zinc-900 outline-none transition placeholder:text-zinc-400 focus:border-navy-700 focus:ring-2 focus:ring-navy-100"
                placeholder="Tempel link postingan lowongan jika ada"
              />
            </label>

            <label className="block">
              <span className="text-sm font-semibold text-zinc-800">Kata kunci penting</span>
              <input
                value={keywordDraft}
                onChange={(event) => setKeywordDraft(event.target.value)}
                onKeyDown={handleKeywordKeyDown}
                onBlur={() => addKeywords()}
                className="mt-2 h-11 w-full rounded-lg border border-zinc-300 bg-white px-3 text-sm text-zinc-900 outline-none transition placeholder:text-zinc-400 focus:border-navy-700 focus:ring-2 focus:ring-navy-100"
                placeholder="Contoh: unpaid, remote, social media, admin, freelance"
              />
              {keywords.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-2">
                  {keywords.map((keyword) => (
                    <button
                      key={keyword}
                      type="button"
                      className="inline-flex items-center gap-1 rounded-full border border-navy-100 bg-navy-50 px-2.5 py-1 text-xs font-semibold text-navy-800"
                      onClick={() => removeKeyword(keyword)}
                    >
                      {keyword}
                      <X className="h-3 w-3" aria-hidden="true" />
                    </button>
                  ))}
                </div>
              )}
            </label>

            {error && (
              <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">
                {error}
              </div>
            )}

            <div className="flex flex-col gap-3 sm:flex-row">
              <button type="submit" className="btn-primary w-full sm:w-auto" disabled={loading}>
                {loading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <ArrowRight className="h-4 w-4" aria-hidden="true" />}
                {loading ? 'Membaca pola lowongan...' : 'Scan Lowongan'}
              </button>
              <button
                type="button"
                className="btn-secondary w-full sm:w-auto"
                onClick={() => {
                  setJobText('');
                  setSourceUrl('');
                  setKeywords([]);
                  setKeywordDraft('');
                  setResult(null);
                  setError('');
                }}
              >
                <RotateCcw className="h-4 w-4" aria-hidden="true" />
                Reset
              </button>
            </div>
          </form>
        </section>

        <aside className="card p-4 lg:col-span-4">
          <h2 className="text-base font-semibold text-zinc-950">Apa yang akan dicek?</h2>
          <div className="mt-3 grid gap-2 text-sm leading-6 text-zinc-700">
            {[
              'Trust Score dan rekomendasi apply.',
              'Red flag seperti biaya, data pribadi, dan janji tidak realistis.',
              'Informasi lowongan yang belum disebutkan.',
              'Checklist aman sebelum mengirim CV atau dokumen.',
            ].map((item) => (
              <div key={item} className="rounded-lg border border-zinc-200 bg-zinc-50 px-3 py-2">
                {item}
              </div>
            ))}
          </div>
        </aside>
      </div>

      {result && (
        <>
          {!isAuthenticated ? (
            <div className="rounded-lg border border-navy-100 bg-navy-50 p-4 text-sm text-navy-900">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <p>Masuk untuk menyimpan hasil scan ini ke riwayat.</p>
                <Link to="/login" className="btn-secondary bg-white">
                  Masuk
                </Link>
              </div>
            </div>
          ) : (
            <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-800">
              Hasil scan otomatis tersimpan ke riwayat akun kamu.
            </div>
          )}
          <ScanResultSections result={result} />
        </>
      )}

      {isAuthenticated && (
        <HistoryDrawer
          open={historyOpen}
          onOpenChange={setHistoryOpen}
          onReuseScan={handleReuseScan}
        />
      )}
    </div>
  );
}
