export default function ResumeTemplateGrid({ templates, onUseTemplate }) {
  return (
    <section className="rw-card">
      <div style={{ marginBottom: "1rem" }}>
        <h3 style={{ fontSize: "1.125rem", fontWeight: 600, color: "#0f172a" }}>Mẫu CV</h3>
        <p style={{ marginTop: "0.25rem", fontSize: "0.875rem", color: "#64748b" }}>
          Chọn một mẫu có sẵn để điền nhanh nội dung thay vì bắt đầu từ form trống.
        </p>
      </div>

      <div className="rw-template-grid">
        {templates.map((template) => (
          <article key={template.slug || template.name} className="rw-template-card">
            <div className="rw-template-thumb">
              {template.thumbnail || template.name.slice(0, 2).toUpperCase()}
            </div>
            <div className="rw-template-body">
              <h4 style={{ fontSize: "1rem", fontWeight: 600, color: "#0f172a" }}>{template.name}</h4>
              <p style={{ marginTop: "0.5rem", fontSize: "0.875rem", lineHeight: "1.5rem", color: "#475569" }}>
                {template.description}
              </p>
              <button type="button" className="btn" style={{ marginTop: "1.25rem" }} onClick={() => onUseTemplate(template)}>
                Dùng mẫu này
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}