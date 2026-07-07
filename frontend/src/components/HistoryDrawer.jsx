import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import {
  deleteScanHistoryItem,
  fetchScanHistory,
  fetchScanHistoryDetail,
} from '../lib/api.js';
import HistoryDetail from './HistoryDetail.jsx';
import HistoryList from './HistoryList.jsx';
import HistoryToolbar from './HistoryToolbar.jsx';

export default function HistoryDrawer({ open, onOpenChange, onReuseScan }) {
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(false);
  const [detailLoading, setDetailLoading] = useState(false);
  const [deletingId, setDeletingId] = useState(null);
  const [error, setError] = useState('');

  async function loadHistory() {
    setLoading(true);
    setError('');
    try {
      const data = await fetchScanHistory();
      setItems(data);
      if (detail && !data.some((item) => item.id === detail.id)) {
        setDetail(null);
      }
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadDetail(id) {
    setDetailLoading(true);
    setError('');
    try {
      const data = await fetchScanHistoryDetail(id);
      setDetail(data);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setDetailLoading(false);
    }
  }

  async function handleDelete(id) {
    setDeletingId(id);
    setError('');
    try {
      await deleteScanHistoryItem(id);
      setItems((current) => current.filter((item) => item.id !== id));
      if (detail?.id === id) setDetail(null);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setDeletingId(null);
    }
  }

  function handleReuse(detailData) {
    if (onReuseScan) {
      onReuseScan(detailData);
    } else {
      navigate('/scanner', { state: { reuseScan: detailData } });
    }
    onOpenChange(false);
  }

  useEffect(() => {
    if (open) loadHistory();
  }, [open]);

  useEffect(() => {
    if (!open) return undefined;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = previousOverflow;
    };
  }, [open]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50">
      <button
        type="button"
        className="absolute inset-0 bg-zinc-950/25"
        onClick={() => onOpenChange(false)}
        aria-label="Tutup riwayat scan"
      />

      <section
        className={[
          'fixed inset-y-0 right-0 z-10 flex h-dvh w-full flex-col overflow-hidden bg-white shadow-soft',
          detail ? 'sm:max-w-[720px]' : 'sm:max-w-[520px]',
        ].join(' ')}
        aria-label="Riwayat scan"
      >
        <HistoryToolbar
          count={items.length}
          loading={loading}
          onRefresh={loadHistory}
          onClose={() => onOpenChange(false)}
        />

        {error && (
          <div className="shrink-0 border-b border-red-200 bg-red-50 px-5 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        <div className="min-h-0 flex-1 overflow-y-auto bg-zinc-50 px-4 py-4 sm:px-5">
          {detail ? (
            <HistoryDetail
              detail={detail}
              loading={detailLoading}
              deleting={deletingId === detail.id}
              onBack={() => setDetail(null)}
              onDelete={handleDelete}
              onReuse={handleReuse}
            />
          ) : loading ? (
            <div className="card p-5 text-sm text-zinc-600">Memuat riwayat...</div>
          ) : (
            <HistoryList
              items={items}
              selectedId={detail?.id}
              onSelect={loadDetail}
              onDelete={handleDelete}
              deletingId={deletingId}
            />
          )}
        </div>
      </section>
    </div>
  );
}
