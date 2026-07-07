import { SearchCheck } from 'lucide-react';

export default function AuthLayout({ title, subtitle, children }) {
  return (
    <section className="bg-zinc-50 py-10 sm:py-14">
      <div className="page-shell flex min-h-[calc(100vh-9rem)] items-center justify-center">
        <div className="card w-full max-w-md p-5 sm:p-6">
          <div className="mb-5 flex items-start gap-3">
            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-navy-800 text-white">
              <SearchCheck className="h-5 w-5" aria-hidden="true" />
            </div>
            <div>
              <h1 className="text-2xl font-semibold tracking-normal text-zinc-950">{title}</h1>
              <p className="mt-1 text-sm leading-6 text-zinc-600">{subtitle}</p>
            </div>
          </div>
          {children}
        </div>
      </div>
    </section>
  );
}
