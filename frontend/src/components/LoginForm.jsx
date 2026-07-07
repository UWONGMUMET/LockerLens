import { Loader2, LogIn } from 'lucide-react';
import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import { useAuth } from '../context/AuthContext.jsx';

export default function LoginForm({ onSwitchMode, notice }) {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    if (!form.email.includes('@')) {
      setError('Masukkan email yang valid.');
      return;
    }
    if (form.password.length < 8) {
      setError('Password minimal 8 karakter.');
      return;
    }
    setLoading(true);
    try {
      await login(form);
      navigate(location.state?.from?.pathname || '/scanner', { replace: true });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {notice && <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-800">{notice}</div>}
      <label className="block">
        <span className="text-sm font-semibold text-zinc-800">Email</span>
        <input
          value={form.email}
          onChange={(event) => setForm((current) => ({ ...current, email: event.target.value }))}
          type="email"
          required
          className="mt-2 h-11 w-full rounded-lg border border-zinc-300 px-3 text-sm outline-none focus:border-navy-700 focus:ring-2 focus:ring-navy-100"
        />
      </label>
      <label className="block">
        <span className="text-sm font-semibold text-zinc-800">Password</span>
        <input
          value={form.password}
          onChange={(event) => setForm((current) => ({ ...current, password: event.target.value }))}
          type="password"
          required
          minLength={8}
          className="mt-2 h-11 w-full rounded-lg border border-zinc-300 px-3 text-sm outline-none focus:border-navy-700 focus:ring-2 focus:ring-navy-100"
        />
      </label>
      {error && <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
      <button type="submit" className="btn-primary w-full" disabled={loading}>
        {loading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <LogIn className="h-4 w-4" aria-hidden="true" />}
        {loading ? 'Memproses...' : 'Masuk'}
      </button>
      <p className="text-center text-sm text-zinc-600">
        Belum punya akun?{' '}
        <button type="button" className="font-semibold text-navy-800 hover:underline" onClick={onSwitchMode}>
          Daftar
        </button>
      </p>
    </form>
  );
}
