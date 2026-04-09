export default function ResumeTemplateGrid({ templates, onUseTemplate }) {
  return (
    <section className="rounded-[24px] border border-slate-200 bg-white p-5 shadow-[0_14px_30px_rgba(15,23,42,0.05)]">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-slate-900">Mẫu CV</h3>
        <p className="mt-1 text-sm text-slate-500">Chọn một mẫu có sẵn để điền nhanh nội dung thay vì bắt đầu từ form trống.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {templates.map((template) => (
          <article key={template.slug || template.name} className="overflow-hidden rounded-[22px] border border-slate-200 bg-slate-50 transition hover:-translate-y-1 hover:border-blue-200 hover:bg-white hover:shadow-[0_18px_34px_rgba(29,78,216,0.10)]">
            <div className="flex aspect-[4/3] items-center justify-center bg-gradient-to-br from-blue-600 via-blue-500 to-sky-400 text-3xl font-extrabold tracking-[0.18em] text-white">
              {template.thumbnail || template.name.slice(0, 2).toUpperCase()}
            </div>
            <div className="p-5">
              <h4 className="text-base font-semibold text-slate-900">{template.name}</h4>
              <p className="mt-2 text-sm leading-6 text-slate-600">{template.description}</p>
              <button type="button" className="btn mt-5 rounded-2xl px-4 py-2 text-sm font-semibold shadow-none" onClick={() => onUseTemplate(template)}>
                Dùng mẫu này
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}