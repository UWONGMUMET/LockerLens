import { Menu, SearchCheck, X } from 'lucide-react';
import { useState } from 'react';
import { NavLink } from 'react-router-dom';

import { useAuth } from '../context/AuthContext.jsx';
import HistoryDrawer from './HistoryDrawer.jsx';
import UserMenu from './UserMenu.jsx';

const guestLinks = [
  { to: '/', label: 'Home' },
  { to: '/scanner', label: 'Scanner' },
  { to: '/safety-guide', label: 'Safety Guide' },
  { to: '/about', label: 'About' },
];

const authLinks = [
  { to: '/', label: 'Home' },
  { to: '/scanner', label: 'Scanner' },
  { to: '/safety-guide', label: 'Safety Guide' },
  { to: '/about', label: 'About' },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const [historyOpen, setHistoryOpen] = useState(false);
  const { isAuthenticated } = useAuth();
  const links = isAuthenticated ? authLinks : guestLinks;

  return (
    <header className="sticky top-0 z-40 border-b border-zinc-200 bg-white/95 backdrop-blur">
      <div className="page-shell flex h-16 items-center justify-between">
        <NavLink to="/" className="flex items-center gap-2 text-lg font-semibold text-zinc-950" onClick={() => setOpen(false)}>
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-navy-800 text-white">
            <SearchCheck className="h-5 w-5" aria-hidden="true" />
          </span>
          <span>LokerLens</span>
        </NavLink>

        <nav className="hidden items-center gap-1 md:flex">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                [
                  'rounded-lg px-3 py-2 text-sm font-medium transition',
                  isActive ? 'bg-zinc-100 text-navy-800' : 'text-zinc-600 hover:bg-zinc-50 hover:text-zinc-950',
                ].join(' ')
              }
            >
              {link.label}
            </NavLink>
          ))}
          {!isAuthenticated && (
            <NavLink
              to="/login"
              className="ml-2 inline-flex items-center justify-center rounded-lg bg-navy-800 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-navy-900"
            >
              Masuk
            </NavLink>
          )}
          {isAuthenticated && <UserMenu onOpenHistory={() => setHistoryOpen(true)} />}
        </nav>

        <button
          type="button"
          className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-zinc-200 text-zinc-700 md:hidden"
          onClick={() => setOpen((value) => !value)}
          aria-label="Toggle navigation"
        >
          {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {open && (
        <div className="border-t border-zinc-200 bg-white md:hidden">
          <nav className="page-shell flex flex-col py-3">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                onClick={() => setOpen(false)}
                className={({ isActive }) =>
                  [
                    'rounded-lg px-3 py-3 text-sm font-medium',
                    isActive ? 'bg-zinc-100 text-navy-800' : 'text-zinc-700',
                  ].join(' ')
                }
              >
                {link.label}
              </NavLink>
            ))}
            {!isAuthenticated && (
              <NavLink
                to="/login"
                onClick={() => setOpen(false)}
                className="mt-2 inline-flex items-center justify-center rounded-lg bg-navy-800 px-4 py-3 text-sm font-semibold text-white transition hover:bg-navy-900"
              >
                Masuk
              </NavLink>
            )}
            {isAuthenticated && (
              <UserMenu
                compact
                onLogout={() => setOpen(false)}
                onOpenHistory={() => {
                  setOpen(false);
                  setHistoryOpen(true);
                }}
              />
            )}
          </nav>
        </div>
      )}
      {isAuthenticated && <HistoryDrawer open={historyOpen} onOpenChange={setHistoryOpen} />}
    </header>
  );
}
