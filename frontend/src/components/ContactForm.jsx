import { Send } from 'lucide-react';
import { useState } from 'react';

import { sendContactMessage } from '../lib/api.js';

const categories = [
  { value: 'feedback', label: 'Feedback' },
  { value: 'campus_partnership', label: 'Partnership kampus' },
  { value: 'employer_verification', label: 'Employer verification' },
  { value: 'other', label: 'Lainnya' },
];

export default function ContactForm() {
  const [form, setForm] = useState({
    name: '',
    email: '',
    category: 'feedback',
    message: '',
  });
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setStatus('');
    setError('');
    setLoading(true);
    try {
      const data = await sendContactMessage(form);
      setStatus(data.message);
      setForm({ name: '', email: '', category: 'feedback', message: '' });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="card space-y-4 p-5">
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block">
          <span className="text-sm font-semibold text-zinc-800">Nama</span>
          <input
            value={form.name}
            onChange={(event) => updateField('name', event.target.value)}
            required
            minLength={2}
            className="mt-2 h-11 w-full rounded-lg border border-zinc-300 px-3 text-sm outline-none focus:border-navy-700 focus:ring-2 focus:ring-navy-100"
          />
        </label>
        <label className="block">
          <span className="text-sm font-semibold text-zinc-800">Email</span>
          <input
            value={form.email}
            onChange={(event) => updateField('email', event.target.value)}
            required
            type="email"
            className="mt-2 h-11 w-full rounded-lg border border-zinc-300 px-3 text-sm outline-none focus:border-navy-700 focus:ring-2 focus:ring-navy-100"
          />
        </label>
      </div>
      <label className="block">
        <span className="text-sm font-semibold text-zinc-800">Pilihan kebutuhan</span>
        <select
          value={form.category}
          onChange={(event) => updateField('category', event.target.value)}
          className="mt-2 h-11 w-full rounded-lg border border-zinc-300 bg-white px-3 text-sm outline-none focus:border-navy-700 focus:ring-2 focus:ring-navy-100"
        >
          {categories.map((category) => (
            <option key={category.value} value={category.value}>{category.label}</option>
          ))}
        </select>
      </label>
      <label className="block">
        <span className="text-sm font-semibold text-zinc-800">Pesan</span>
        <textarea
          value={form.message}
          onChange={(event) => updateField('message', event.target.value)}
          required
          minLength={10}
          rows={7}
          className="mt-2 w-full resize-y rounded-lg border border-zinc-300 p-3 text-sm leading-6 outline-none focus:border-navy-700 focus:ring-2 focus:ring-navy-100"
        />
      </label>
      {status && <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">{status}</div>}
      {error && <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
      <button type="submit" className="btn-primary" disabled={loading}>
        <Send className="h-4 w-4" aria-hidden="true" />
        {loading ? 'Menyimpan pesan...' : 'Kirim Pesan'}
      </button>
    </form>
  );
}
