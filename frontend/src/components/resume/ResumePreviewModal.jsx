function PreviewSection({ title, children }) {
  return (
    <section className="rw-preview-section">
      <h4>{title}</h4>
      <div className="rw-pre-wrap rw-preview-content">{children}</div>
    </section>
  );
}

function toListText(value) {
  if (Array.isArray(value)) {
    return value.filter(Boolean).map(String).join(" • ");
  }
  if (typeof value === "string") {
    return value.trim();
  }
  return "";
}

export default function ResumePreviewModal({ resume, onClose, onDownload }) {
  const structured = resume.structured_json || {};
  const template = structured.template || {};
  const skills = toListText(structured.skills);
  const sourceLabel = resume.source_type === "upload" ? "CV upload" : "Tạo từ mẫu";

  return (
    <div className="rw-modal-backdrop">
      <div className="rw-preview-modal">
        <div className="rw-modal-head">
          <div>
            <p className="rw-modal-kicker">Xem trước CV</p>
            <h3 className="rw-heading-2xl">{resume.title}</h3>
            <p className="rw-modal-subtitle">
              Mẫu: {resume.template_name || template.name || "Chưa chọn"} • {sourceLabel}
            </p>
          </div>
          <div className="rw-modal-actions">
            <button type="button" className="rw-btn-outline-lg" onClick={() => onDownload?.(resume)}>
              Tải PDF
            </button>
            <button type="button" className="rw-btn-close" onClick={onClose}>
              Đóng
            </button>
          </div>
        </div>

        <div className="rw-modal-body">
          <PreviewSection title="Thông tin cơ bản">
            <p><strong>Họ tên:</strong> {structured.full_name || "Chưa cập nhật"}</p>
            <p><strong>Email:</strong> {structured.email || "Chưa cập nhật"}</p>
            <p><strong>Số điện thoại:</strong> {structured.phone || "Chưa cập nhật"}</p>
            <p><strong>Headline:</strong> {structured.headline || "Chưa cập nhật"}</p>
          </PreviewSection>

          <PreviewSection title="Tóm tắt">
            {structured.summary || "Chưa có nội dung"}
          </PreviewSection>

          <PreviewSection title="Kỹ năng">
            {skills || "Chưa có nội dung"}
          </PreviewSection>

          <PreviewSection title="Kinh nghiệm">
            {structured.experience || "Chưa có nội dung"}
          </PreviewSection>

          <PreviewSection title="Học vấn">
            {structured.education || "Chưa có nội dung"}
          </PreviewSection>
        </div>
      </div>
    </div>
  );
}
