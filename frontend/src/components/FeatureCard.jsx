export default function FeatureCard({ title, description, icon: Icon }) {
  return (
    <article className="card p-5">
      <div className="flex h-11 w-11 items-center justify-center rounded-lg bg-navy-50 text-navy-800">
        <Icon className="h-5 w-5" aria-hidden="true" />
      </div>
      <h3 className="mt-4 text-base font-semibold text-zinc-950">{title}</h3>
      <p className="mt-2 text-sm leading-6 text-zinc-600">{description}</p>
    </article>
  );
}
