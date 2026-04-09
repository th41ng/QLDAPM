export default function ResumeForm({ values, onChange, onSaveDraft, onPreview, onSubmit, saving, editingTitle }) {
  return (
    <form
      style={{ display: "grid", gap: "1.25rem" }}
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit();
      }}
    >
      <section className="rw-card">
        <div className="rw-flex-between" style={{ marginBottom: "1rem" }}>
          <div>
            <h3 style={{ fontSize: "1.125rem", fontWeight: 600, color: "#0f172a" }}>{editingTitle || "Tạo CV từ UI"}</h3>
            <p style={{ marginTop: "0.25rem", fontSize: "0.875rem", color: "#64748b" }}>Chia form thành từng section để dễ viết và dễ scan lại trước khi lưu.</p>
          </div>
          <span className="rw-badge rw-badge-blue">UI Resume</span>
        </div>
        <SectionTitle title="Thông tin cơ bản" description="Thiết lập tiêu đề CV và phần giới thiệu ngắn ở đầu hồ sơ." />
        <div className="rw-grid-2">
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

      <section className="rw-card">
        <SectionTitle title="Summary" description="Tóm tắt 3-5 dòng về định hướng nghề nghiệp, điểm mạnh và loại công việc bạn đang tìm." />
        <Field label="Tổng quan">
          <textarea rows="5" value={values.summary} onChange={(event) => onChange("summary", event.target.value)} placeholder="Giới thiệu ngắn về kinh nghiệm, năng lực nổi bật và mục tiêu của bạn..." />
        </Field>
      </section>

      <section className="rw-card">
        <SectionTitle title="Skills" description="Liệt kê kỹ năng chính theo nhóm, cách nhau bằng dấu phẩy để dùng lại cho matching và hiển thị." />
        <Field label="Kỹ năng">
          <input value={values.skills} onChange={(event) => onChange("skills", event.target.value)} placeholder="React, JavaScript, CSS, REST API" />
        </Field>
      </section>

      <section className="rw-card">
        <SectionTitle title="Experience" description="Mô tả kinh nghiệm theo format ngắn gọn, tập trung thành tựu và kết quả thay vì chỉ liệt kê nhiệm vụ." />
        <Field label="Kinh nghiệm">
          <textarea rows="6" value={values.experience} onChange={(event) => onChange("experience", event.target.value)} placeholder="Frontend Developer | ABC Company | 2023-2025..." />
        </Field>
      </section>

      <section className="rw-card">
        <SectionTitle title="Education" description="Ghi học vấn, chứng chỉ hoặc khóa học liên quan nếu có." />
        <Field label="Học vấn">
          <textarea rows="5" value={values.education} onChange={(event) => onChange("education", event.target.value)} placeholder="Đại học..., chuyên ngành..., chứng chỉ..." />
        </Field>
      </section>

      <div className="rw-form-actions">
        <button type="button" className="rw-btn-outline-lg" onClick={onSaveDraft}>
          Lưu nháp
        </button>
        <button type="button" className="rw-btn-preview" onClick={onPreview}>
          Xem trước
        </button>
        <button type="submit" className="btn" disabled={saving}>
          {saving ? "Đang lưu..." : "Lưu CV"}
        </button>
      </div>
    </form>
  );
}

function SectionTitle({ title, description }) {
  return (
    <div className="rw-section-divider">
      <h4 style={{ fontSize: "1rem", fontWeight: 600, color: "#0f172a" }}>{title}</h4>
      <p style={{ marginTop: "0.25rem", fontSize: "0.875rem", lineHeight: "1.5rem", color: "#64748b" }}>{description}</p>
    </div>
  );
}

function Field({ label, children, full }) {
  return (
    <label className={full ? "rw-field-full" : "rw-field"}>
      <span className="rw-label-sm">{label}</span>
      {children}
    </label>
  );
}