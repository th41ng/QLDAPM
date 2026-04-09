export default function ResumeStats({ resumes }) {
  const manualCount = resumes.filter((resume) => resume.source_type === "manual").length;
  const uploadCount = resumes.filter((resume) => resume.source_type === "upload").length;
  const primaryCount = resumes.filter((resume) => resume.is_primary).length;

  const cards = [
    { label: "CV đã tạo", value: manualCount, tone: "text-blue-700 bg-blue-50 border-blue-100" },
    { label: "CV đã upload", value: uploadCount, tone: "text-emerald-700 bg-emerald-50 border-emerald-100" },
    { label: "CV đang dùng ứng tuyển", value: primaryCount, tone: "text-violet-700 bg-violet-50 border-violet-100" },
  ];

  return (
    <section className="grid gap-4 md:grid-cols-3">
      {cards.map((card) => (
        <article key={card.label} className={`rounded-[24px] border p-5 shadow-[0_14px_30px_rgba(15,23,42,0.05)] ${card.tone}`}>
          <span className="text-sm font-medium opacity-80">{card.label}</span>
          <strong className="mt-3 block text-3xl font-semibold tracking-tight">{String(card.value).padStart(2, "0")}</strong>
        </article>
      ))}
    </section>
  );
}