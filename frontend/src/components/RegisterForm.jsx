import { Loader2, UserPlus } from 'lucide-react';
import { useState } from 'react';

import { useAuth } from '../context/AuthContext.jsx';

export default function RegisterForm({ onSwitchMode, onRegistered }) {
  const { register } = useAuth();
  const [form, setForm] = useState({ name: '', email: '', password: '', confirmPassword: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    if (form.name.trim().length < 2) {
      setError('Nama minimal 2 karakter.');
      return;
    }
    if (!form.email.includes('@')) {
      setError('Masukkan email yang valid.');
      return;
    }
    if (form.password.length < 8) {
      setError('Password minimal 8 karakter.');
      return;
    }
    if (form.password !== form.confirmPassword) {
      setError('Confirm password harus sama.');
      return;
    }
    setLoading(true);
    try {
      await register({ name: form.name, email: form.email, password: form.password });
      setForm({ name: '', email: form.email, password: '', confirmPassword: '' });
      onRegistered?.();
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <label className="block">
        <span className="text-sm font-semibold text-zinc-800">Nama</span>
        <input
          value={form.name}
          onChange={(event) => updateField('name', event.target.value)}
          required
          className="mt-2 h-11 w-full rounded-lg border border-zinc-300 px-3 text-sm outline-none focus:border-navy-700 focus:ring-2 focus:ring-navy-100"
        />
      </label>
      <label className="block">
        <span className="text-sm font-semibold text-zinc-800">Email</span>
        <input
          value={form.email}
          onChange={(event) => updateField('email', event.target.value)}
          type="email"
          required
          className="mt-2 h-11 w-full rounded-lg border border-zinc-300 px-3 text-sm outline-none focus:border-navy-700 focus:ring-2 focus:ring-navy-100"
        />
      </label>
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block">
          <span className="text-sm font-semibold text-zinc-800">Password</span>
          <input
            value={form.password}
            onChange={(event) => updateField('password', event.target.value)}
            type="password"
            required
            minLength={8}
            className="mt-2 h-11 w-full rounded-lg border border-zinc-300 px-3 text-sm outline-none focus:border-navy-700 focus:ring-2 focus:ring-navy-100"
          />
        </label>
        <label className="block">
          <span className="text-sm font-semibold text-zinc-800">Confirm password</span>
          <input
            value={form.confirmPassword}
            onChange={(event) => updateField('confirmPassword', event.target.value)}
            type="password"
            required
            minLength={8}
            className="mt-2 h-11 w-full rounded-lg border border-zinc-300 px-3 text-sm outline-none focus:border-navy-700 focus:ring-2 focus:ring-navy-100"
          />
        </label>
      </div>
      {error && <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
      <button type="submit" className="btn-primary w-full" disabled={loading}>
        {loading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <UserPlus className="h-4 w-4" aria-hidden="true" />}
        {loading ? 'Mendaftarkan...' : 'Daftar'}
      </button>
      <p className="text-center text-sm text-zinc-600">
        Sudah punya akun?{' '}
        <button type="button" className="font-semibold text-navy-800 hover:underline" onClick={onSwitchMode}>
          Masuk
        </button>
      </p>
    </form>
  );
}
