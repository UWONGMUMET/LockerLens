import { useEffect, useState } from 'react';

import ProfileCard from '../components/ProfileCard.jsx';
import { fetchProfile } from '../lib/api.js';

export default function ProfilePage() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    async function run() {
      try {
        const data = await fetchProfile();
        if (active) setProfile(data);
      } catch (requestError) {
        if (active) setError(requestError.message);
      } finally {
        if (active) setLoading(false);
      }
    }
    run();
    return () => {
      active = false;
    };
  }, []);

  return (
    <section className="bg-zinc-50 py-14">
      <div className="page-shell">
        {error && <div className="mb-6 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
        {loading ? <div className="card p-6 text-sm text-zinc-600">Memuat profile...</div> : <ProfileCard profile={profile} />}
      </div>
    </section>
  );
}
