const SECTION_CLASS = "rounded-[24px] border border-slate-200 bg-white p-5 shadow-[0_14px_30px_rgba(15,23,42,0.05)]";

export default function ResumeForm({ values, onChange, onSaveDraft, onPreview, onSubmit, saving, editingTitle }) {
  return (
    <form
      className="grid gap-5"
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit();
      }}
    >
      <section className={SECTION_CLASS}>
        <div className="mb-4 flex items-center justify-between gap-3">
          <div>
            <h3 className="text-lg font-semibold text-slate-900">{editingTitle || "Tạo CV từ UI"}</h3>
            <p className="mt-1 text-sm text-slate-500">Chia form thành từng section để dễ viết và dễ scan lại trước khi lưu.</p>
          </div>
          <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">UI Resume</span>
        </div>

        <SectionTitle title="Thông tin cơ bản" description="Thiết lập tiêu đề CV và phần giới thiệu ngắn ở đầu hồ sơ." />
        <div className="grid gap-4 md:grid-cols-2">
          <Field label="Tiêu đề CV">
            <input value={values.title} onChange={(event) => onChange("title", event.target.value)} placeholder="Ví dụ: CV Frontend React" />
          </Field>
          <Field label="Full name">
            <input value={values.full_name} onChange={(event) => onChange("full_name", event.target.value)} placeholder="Nguyễn Văn A" />
          </Field>
          <Field label="Headline" full>
            <input value={values.headline} onChange={(event) => onChange("headline", event.target.value)} placeholder="Frontend Developer | React | 2 năm kinh nghiệm" />
          </Field>
        </div>
      </section>

      <section className={SECTION_CLASS}>
        <SectionTitle title="Summary" description="Tóm tắt 3-5 dòng về định hướng nghề nghiệp, điểm mạnh và loại công việc bạn đang tìm." />
        <Field label="Tổng quan">
          <textarea rows="5" value={values.summary} onChange={(event) => onChange("summary", event.target.value)} placeholder="Giới thiệu ngắn về kinh nghiệm, năng lực nổi bật và mục tiêu của bạn..." />
        </Field>
      </section>

      <section className={SECTION_CLASS}>
        <SectionTitle title="Skills" description="Liệt kê kỹ năng chính theo nhóm, cách nhau bằng dấu phẩy để dùng lại cho matching và hiển thị." />
        <Field label="Kỹ năng">
          <input value={values.skills} onChange={(event) => onChange("skills", event.target.value)} placeholder="React, JavaScript, TailwindCSS, REST API" />
        </Field>
      </section>

      <section className={SECTION_CLASS}>
        <SectionTitle title="Experience" description="Mô tả kinh nghiệm theo format ngắn gọn, tập trung thành tựu và kết quả thay vì chỉ liệt kê nhiệm vụ." />
        <Field label="Kinh nghiệm">
          <textarea rows="6" value={values.experience} onChange={(event) => onChange("experience", event.target.value)} placeholder="Frontend Developer | ABC Company | 2023-2025..." />
        </Field>
      </section>

      <section className={SECTION_CLASS}>
        <SectionTitle title="Education" description="Ghi học vấn, chứng chỉ hoặc khóa học liên quan nếu có." />
        <Field label="Học vấn">
          <textarea rows="5" value={values.education} onChange={(event) => onChange("education", event.target.value)} placeholder="Đại học..., chuyên ngành..., chứng chỉ..." />
        </Field>
      </section>

      <div className="flex flex-wrap items-center justify-end gap-3">
        <button type="button" className="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-blue-200 hover:text-blue-700" onClick={onSaveDraft}>
          Lưu nháp
        </button>
        <button type="button" className="rounded-2xl border border-blue-200 bg-blue-50 px-5 py-3 text-sm font-semibold text-blue-700 transition hover:bg-blue-100" onClick={onPreview}>
          Xem trước
        </button>
        <button type="submit" className="btn rounded-2xl px-5 py-3 text-sm font-semibold shadow-none" disabled={saving}>
          {saving ? "Đang lưu..." : "Lưu CV"}
        </button>
      </div>
    </form>
  );
}

function SectionTitle({ title, description }) {
  return (
    <div className="mb-4 border-b border-slate-100 pb-4">
      <h4 className="text-base font-semibold text-slate-900">{title}</h4>
      <p className="mt-1 text-sm leading-6 text-slate-500">{description}</p>
    </div>
  );
}

function Field({ label, children, full }) {
  return (
    <label className={`grid gap-2 ${full ? "md:col-span-2" : ""}`}>
      <span className="text-sm font-semibold text-slate-700">{label}</span>
      {children}
    </label>
  );
}