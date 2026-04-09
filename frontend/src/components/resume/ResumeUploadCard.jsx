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

export default function ResumeUploadCard({ file, uploads, onPickFile, onSubmitUpload, busy }) {
  return (
    <div style={{ display: "grid", gap: "1rem" }}>
      <section className="rw-card">
        <div className="rw-upload-zone">
          <div className="rw-upload-icon">↑</div>
          <h3 style={{ marginTop: "1rem", fontSize: "1.125rem", fontWeight: 600, color: "#0f172a" }}>Upload CV có sẵn</h3>
          <p style={{ marginTop: "0.5rem", fontSize: "0.875rem", lineHeight: "1.5rem", color: "#475569" }}>
            Kéo thả file vào đây hoặc chọn file từ máy của bạn. Hệ thống hỗ trợ CV PDF, DOC và DOCX.
          </p>
          <div className="rw-upload-formats">
            <span className="rw-upload-format-chip">PDF</span>
            <span className="rw-upload-format-chip">DOC</span>
            <span className="rw-upload-format-chip">DOCX</span>
          </div>
          <div className="rw-upload-actions">
            <label className="rw-upload-pick-label">
              Chọn file
              <input type="file" accept=".pdf,.doc,.docx" style={{ display: "none" }} onChange={(event) => onPickFile(event.target.files?.[0] || null)} />
            </label>
            <button type="button" className="btn" onClick={onSubmitUpload} disabled={!file || busy}>
              {busy ? "Đang upload..." : "Upload CV"}
            </button>
          </div>
          <p style={{ marginTop: "0.75rem", fontSize: "0.875rem", color: "#64748b" }}>
            {file ? `Đã chọn: ${file.name}` : "Chưa chọn file nào"}
          </p>
        </div>
      </section>

      <section className="rw-card">
        <div className="rw-flex-between">
          <h3 style={{ fontSize: "1rem", fontWeight: 600, color: "#0f172a" }}>Upload gần đây</h3>
          <span style={{ fontSize: "0.75rem", fontWeight: 500, color: "#64748b" }}>{uploads.length} file</span>
        </div>
        <div style={{ marginTop: "1rem", display: "grid", gap: "0.75rem" }}>
          {uploads.length ? (
            uploads.map((resume) => (
              <div key={resume.id} className="rw-upload-row">
                <strong style={{ display: "block", fontSize: "0.875rem", fontWeight: 600, color: "#0f172a" }}>{resume.title}</strong>
                <div className="rw-upload-row-meta">
                  <span>{resume.original_filename || resume.file_ext || "CV upload"}</span>
                  <span>{formatDate(resume.updated_at)}</span>
                </div>
              </div>
            ))
          ) : (
            <p className="rw-resume-empty" style={{ padding: "1.25rem 1rem" }}>Chưa có file upload gần đây.</p>
          )}
        </div>
      </section>

      <section className="rw-tips-card">
        <h3 style={{ fontSize: "1rem", fontWeight: 600, color: "#0f172a" }}>Mẹo tạo CV</h3>
        <ul className="rw-tips-list">
          <li>Đặt tiêu đề CV theo vị trí bạn muốn ứng tuyển để dễ quản lý.</li>
          <li>Headline nên ngắn, rõ năng lực chính và số năm kinh nghiệm.</li>
          <li>Dùng một CV chính làm bản đang ứng tuyển để thao tác nhanh ở các job detail.</li>
        </ul>
      </section>
    </div>
  );
}