function formatDate(value) {
  if (!value) return "Chưa cập nhật";
  try {
    return new Date(value).toLocaleDateString("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  } catch {
    return "Chưa cập nhật";
  }
}

function getStatus(resume) {
  if (resume.is_primary) return { label: "Đang dùng", cls: "rw-badge rw-badge-blue" };
  if (resume.source_type === "upload") return { label: "Đã upload", cls: "rw-badge rw-badge-green" };
  return { label: "Sẵn sàng", cls: "rw-badge rw-badge-slate" };
}

export default function ResumeList({ resumes, onView, onEdit, onDelete, exportUrl }) {
  return (
    <section className="rw-card">
      <div className="rw-flex-between" style={{ marginBottom: "1rem" }}>
        <div>
          <h3 style={{ fontSize: "1.125rem", fontWeight: 600, color: "#0f172a" }}>Danh sách CV</h3>
          <p style={{ marginTop: "0.25rem", fontSize: "0.875rem", color: "#64748b" }}>Quản lý toàn bộ CV tạo từ UI và CV tải lên trong cùng một nơi.</p>
        </div>
        <span className="rw-badge rw-badge-slate">{resumes.length} CV</span>
      </div>

      <div style={{ display: "grid", gap: "1rem" }}>
        {resumes.length ? (
          resumes.map((resume) => {
            const status = getStatus(resume);
            return (
              <article key={resume.id} className="rw-resume-card">
                <div className="rw-resume-card-layout">
                  <div style={{ minWidth: 0 }}>
                    <div style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: "0.5rem" }}>
                      <h4 style={{ fontSize: "1.125rem", fontWeight: 600, color: "#0f172a" }}>{resume.title}</h4>
                      <span className={status.cls}>{status.label}</span>
                      <span className="rw-badge rw-badge-white">
                        {resume.source_type === "upload" ? "Upload" : "Tạo từ UI"}
                      </span>
                    </div>
                    <div style={{ marginTop: "0.5rem", display: "flex", flexWrap: "wrap", gap: "0.5rem 1.25rem", fontSize: "0.875rem", color: "#64748b" }}>
                      <span>Cập nhật: {formatDate(resume.updated_at)}</span>
                      <span>Mẫu: {resume.template_name || "Chưa chọn"}</span>
                      <span>Tag: {(resume.tags || []).length ? resume.tags.map((tag) => tag.name).join(", ") : "Chưa gắn tag"}</span>
                    </div>
                  </div>

                  <div className="rw-resume-actions">
                    <button type="button" className="rw-btn-outline" onClick={() => onView(resume)}>Xem</button>
                    <button type="button" className="rw-btn-outline" onClick={() => onEdit(resume)}>Sửa</button>
                    <a className="rw-btn-outline" href={exportUrl(resume.id, "pdf")} target="_blank" rel="noreferrer">Tải xuống</a>
                    <button type="button" className="rw-btn-danger" onClick={() => onDelete(resume)}>Xóa</button>
                  </div>
                </div>
              </article>
            );
          })
        ) : (
          <div className="rw-resume-empty">
            Chưa có CV nào. Hãy tạo CV mới hoặc upload một file CV sẵn có.
          </div>
        )}
      </div>
    </section>
  );
}