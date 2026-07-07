import ContactForm from '../components/ContactForm.jsx';

export default function ContactPage() {
  return (
    <section className="bg-zinc-50 py-14">
      <div className="page-shell grid gap-8 lg:grid-cols-[0.85fr_1.15fr] lg:items-start">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wide text-navy-800">Contact</p>
          <h1 className="mt-3 text-3xl font-semibold tracking-normal text-zinc-950 sm:text-4xl">
            Partnership atau feedback
          </h1>
          <p className="mt-4 text-base leading-7 text-zinc-600">
            Kirim masukan, ajakan partnership kampus, atau kebutuhan employer verification. Pesan akan tersimpan di backend LokerLens.
          </p>
        </div>
        <ContactForm />
      </div>
    </section>
  );
}
