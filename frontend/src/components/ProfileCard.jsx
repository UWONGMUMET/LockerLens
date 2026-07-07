import { BarChart3, CalendarDays, ShieldAlert, UserRound } from 'lucide-react';

export default function ProfileCard({ profile }) {
  if (!profile) return null;

  const stats = [
    ['Total scan tersimpan', profile.total_scans, BarChart3],
    ['Rata-rata Trust Score', profile.average_trust_score ?? '-', BarChart3],
    ['Risk level paling sering', profile.most_common_risk_level || '-', ShieldAlert],
    ['Scan risiko tinggi', profile.high_risk_scans, ShieldAlert],
  ];

  return (
    <section className="card p-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <div className="flex items-center gap-2 text-sm font-semibold text-zinc-600">
            <UserRound className="h-4 w-4" aria-hidden="true" />
            Profile
          </div>
          <h1 className="mt-3 text-3xl font-semibold tracking-normal text-zinc-950">{profile.user.name}</h1>
          <p className="mt-1 text-sm text-zinc-600">{profile.user.email}</p>
        </div>
        <div className="rounded-lg border border-zinc-200 bg-zinc-50 px-3 py-2 text-sm text-zinc-700">
          <CalendarDays className="mr-2 inline h-4 w-4 text-navy-800" aria-hidden="true" />
          Join {new Date(profile.joined_at).toLocaleDateString('id-ID')}
        </div>
      </div>

      {profile.total_scans === 0 ? (
        <div className="mt-6 rounded-lg border border-zinc-200 bg-zinc-50 p-4 text-sm leading-6 text-zinc-600">
          Kamu belum menyimpan hasil scan. Mulai scan lowongan untuk melihat ringkasan profil risiko.
        </div>
      ) : (
        <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map(([label, value, Icon]) => (
            <div key={label} className="rounded-lg border border-zinc-200 bg-zinc-50 p-4">
              <Icon className="h-5 w-5 text-navy-800" aria-hidden="true" />
              <p className="mt-3 text-xs font-semibold uppercase tracking-wide text-zinc-500">{label}</p>
              <p className="mt-1 text-xl font-semibold text-zinc-950">{value}</p>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
