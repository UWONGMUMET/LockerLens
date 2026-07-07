import { ChevronDown, History, LogOut, UserRound } from 'lucide-react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { useAuth } from '../context/AuthContext.jsx';

export default function UserMenu({ compact = false, onLogout, onOpenHistory }) {
  const { user, logout } = useAuth();
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    onLogout?.();
    navigate('/');
  }

  function goToProfile() {
    setOpen(false);
    onLogout?.();
    navigate('/profile');
  }

  function openHistory() {
    setOpen(false);
    onOpenHistory?.();
  }

  if (compact) {
    return (
      <div className="mt-2 grid gap-2 border-t border-zinc-200 pt-3">
        <button type="button" className="btn-secondary w-full justify-start" onClick={openHistory}>
          <History className="h-4 w-4" aria-hidden="true" />
          Riwayat Scan
        </button>
        <button type="button" className="btn-secondary w-full justify-start" onClick={goToProfile}>
          <UserRound className="h-4 w-4" aria-hidden="true" />
          Profil
        </button>
        <button type="button" className="btn-secondary w-full justify-start" onClick={handleLogout}>
          <LogOut className="h-4 w-4" aria-hidden="true" />
          Keluar
        </button>
      </div>
    );
  }

  return (
    <div className="relative">
      <button
        type="button"
        className="inline-flex items-center gap-2 rounded-lg border border-zinc-200 bg-zinc-50 px-3 py-2 text-sm font-semibold text-zinc-800 transition hover:border-navy-700 hover:text-navy-800"
        onClick={() => setOpen((value) => !value)}
        aria-expanded={open}
      >
        {user && (
          <>
            <UserRound className="h-4 w-4 text-navy-800" aria-hidden="true" />
            <span className="max-w-[9rem] truncate">{user.name}</span>
          </>
        )}
        <ChevronDown className={`h-4 w-4 text-zinc-500 transition ${open ? 'rotate-180' : ''}`} aria-hidden="true" />
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-52 overflow-hidden rounded-lg border border-zinc-200 bg-white p-2 shadow-soft">
          <button type="button" className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-left text-sm font-medium text-zinc-700 hover:bg-zinc-50" onClick={openHistory}>
            <History className="h-4 w-4 text-navy-800" aria-hidden="true" />
            Riwayat Scan
          </button>
          <button type="button" className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-left text-sm font-medium text-zinc-700 hover:bg-zinc-50" onClick={goToProfile}>
            <UserRound className="h-4 w-4 text-navy-800" aria-hidden="true" />
            Profil
          </button>
          <button type="button" className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-left text-sm font-medium text-red-700 hover:bg-red-50" onClick={handleLogout}>
            <LogOut className="h-4 w-4" aria-hidden="true" />
            Keluar
          </button>
        </div>
      )}
    </div>
  );
}
