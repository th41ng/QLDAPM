export default function ResumeTemplateGrid({ templates, onUseTemplate, selectedSlug = "" }) {
  return (
    <section className="rw-card rw-template-grid-shell">
      <div className="rw-template-grid-head">
        <div>
          <h3 className="rw-template-grid-title">Mẫu CV từ database</h3>
          <p className="rw-template-grid-desc">
            Chọn một mẫu thật từ bảng <code>cv_templates</code> để bắt đầu tạo CV từ dữ liệu của bạn.
          </p>
        </div>
        <div className="rw-template-grid-note">
          <strong>{templates.length}</strong>
          <span>mẫu đang hoạt động</span>
        </div>
      </div>

      {templates.length ? (
        <div className="rw-template-grid">
          {templates.map((template) => {
            const selected = selectedSlug && template.slug === selectedSlug;
            return (
              <article
                key={template.id || template.slug || template.name}
                className={selected ? "rw-template-card rw-template-card--gallery rw-template-card--selected" : "rw-template-card rw-template-card--gallery"}
              >
                <div className="rw-template-thumb rw-template-thumb--gallery">
                  {template.thumbnail_url ? (
                    <img src={template.thumbnail_url} alt={template.name} className="rw-template-thumb-media" />
                  ) : template.preview_url ? (
                    <iframe
                      src={template.preview_url}
                      title={`${template.name} preview`}
                      className="rw-template-thumb-media rw-template-thumb-frame"
                    />
                  ) : (
                    <div className="rw-template-thumb-fallback">{template.name.slice(0, 2).toUpperCase()}</div>
                  )}
                  <div className="rw-template-thumb-overlay">
                    <div className="rw-template-thumb-badge">
                      <span>{selected ? "Đang chọn" : template.file_format || "pdf"}</span>
                    </div>
                    {template.preview_url ? (
                      <a className="rw-template-thumb-link" href={template.preview_url} target="_blank" rel="noreferrer">
                        Xem PDF
                      </a>
                    ) : null}
                  </div>
                </div>

                <div className="rw-template-body rw-template-body--gallery">
                  <div className="rw-template-copy">
                    <h4>{template.name}</h4>
                    <p>{template.summary || template.description || "Chưa có mô tả"}</p>
                  </div>

                  <div className="rw-template-meta">
                    <span className="rw-badge rw-badge-white">{template.file_format || "pdf"}</span>
                    <span className="rw-template-meta-link">{template.preview_url ? "Có PDF mẫu" : "Chưa có PDF"}</span>
                  </div>

                  <div className="rw-template-actions">
                    <button
                      type="button"
                      className={selected ? "rw-btn-outline-lg rw-btn-outline-lg--selected" : "rw-btn-outline-lg"}
                      onClick={() => onUseTemplate(template)}
                    >
                      {selected ? "Đã chọn" : "Dùng mẫu này"}
                    </button>
                    {template.preview_url ? (
                      <a className="rw-btn-outline-lg rw-btn-outline-lg--ghost" href={template.preview_url} target="_blank" rel="noreferrer">
                        Mở PDF
                      </a>
                    ) : null}
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      ) : (
        <div className="rw-state-empty">
          <h3>Chưa có mẫu CV nào</h3>
          <p>Hiện tại chưa có dữ liệu trong bảng cv_templates.</p>
        </div>
      )}
    </section>
  );
}
