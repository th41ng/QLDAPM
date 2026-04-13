function getTemplateVariant(template) {
  const key = String(template?.slug || template?.name || "")
    .toLowerCase()
    .trim();
  if (key.includes("ats")) return "ats";
  if (key.includes("creative") || key.includes("minimal")) return "creative";
  return "modern";
}

function getTemplateSkin(template) {
  const key = String(template?.slug || template?.name || "")
    .toLowerCase()
    .trim();
  if (key.includes("modern-blue")) return "modern-blue";
  if (key.includes("ats-clean")) return "ats-clean";
  if (key.includes("creative-minimal")) return "creative-minimal";
  if (key.includes("product-designer")) return "product-designer";
  if (key.includes("data-analyst")) return "data-analyst";
  if (key.includes("hr-executive")) return "hr-executive";
  if (key.includes("marketing-pro")) return "marketing-pro";
  if (key.includes("minimal") || key.includes("executive")) return "minimal-slate";
  return "generic";
}

function getSkinMeta(skin) {
  const meta = {
    "modern-blue": { title: "Tech", cue: "2 cot" },
    "ats-clean": { title: "ATS", cue: "text-first" },
    "creative-minimal": { title: "Creative", cue: "portfolio" },
    "product-designer": { title: "Design", cue: "case-study" },
    "data-analyst": { title: "Data", cue: "metrics" },
    "hr-executive": { title: "Executive", cue: "leadership" },
    "marketing-pro": { title: "Marketing", cue: "campaign" },
    "minimal-slate": { title: "Minimal", cue: "clean" },
    generic: { title: "Template", cue: "flex" },
  };
  return meta[skin] || meta.generic;
}

function getVariantLabel(variant) {
  if (variant === "ats") return "ATS Pro";
  if (variant === "creative") return "Creative";
  return "Modern";
}

export default function ResumeTemplateGrid({ templates, onUseTemplate, selectedSlug = "" }) {
  return (
    <section className="rw-card rw-template-grid-shell">
      <div className="rw-template-grid-head">
        <div>
          <h3 className="rw-template-grid-title">Mẫu CV từ database</h3>
          <p className="rw-template-grid-desc">
            Chọn một mẫu từ bảng <code>cv_templates</code> để dựng CV realtime bằng React template.
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
            const variant = getTemplateVariant(template);
            const skin = getTemplateSkin(template);
            const skinMeta = getSkinMeta(skin);
            return (
              <article
                key={template.id || template.slug || template.name}
                className={selected ? `rw-template-card rw-template-card--gallery rw-template-card--${variant} rw-template-card--skin-${skin} rw-template-card--selected` : `rw-template-card rw-template-card--gallery rw-template-card--${variant} rw-template-card--skin-${skin}`}
              >
                <div className="rw-template-thumb rw-template-thumb--gallery">
                  {template.thumbnail_url ? (
                    <img src={template.thumbnail_url} alt={template.name} className="rw-template-thumb-media" />
                  ) : (
                    <div className="rw-template-thumb-fallback">{template.name.slice(0, 2).toUpperCase()}</div>
                  )}
                  <div className="rw-template-thumb-overlay">
                    <div className="rw-template-thumb-badge">
                      <span>{selected ? "Dang chon" : "Template React"}</span>
                    </div>
                    <span className={`rw-template-variant rw-template-variant--${variant}`}>{getVariantLabel(variant)}</span>
                  </div>
                  <div className="rw-template-motif-row">
                    <span className="rw-template-motif">{skinMeta.title}</span>
                    <span className="rw-template-motif">{skinMeta.cue}</span>
                  </div>
                </div>

                <div className="rw-template-body rw-template-body--gallery">
                  <div className="rw-template-copy">
                    <h4>{template.name}</h4>
                    <p>{template.summary || template.description || "Chưa có mô tả"}</p>
                  </div>

                  <div className="rw-template-meta">
                    <span className="rw-badge rw-badge-white">{template.slug || "template"}</span>
                    <span className="rw-template-meta-link">Live preview {getVariantLabel(variant)}</span>
                  </div>

                  <div className="rw-template-actions">
                    <button
                      type="button"
                      className={selected ? "rw-btn-outline-lg rw-btn-outline-lg--selected rw-template-action-btn" : "rw-btn-outline-lg rw-template-action-btn"}
                      onClick={() => onUseTemplate(template)}
                    >
                      {selected ? "Da chon" : "Chon mau nay"}
                    </button>
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
