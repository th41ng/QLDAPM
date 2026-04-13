function getText(value, fallback = "Chua cap nhat") {
  const text = String(value ?? "").trim();
  return text || fallback;
}

function getRows(value) {
  return String(value ?? "")
    .split(/\n/)
    .map((item) => item.trim())
    .filter(Boolean);
}

export default function ATSCleanTemplate({ data = {} }) {
  const skillRows = getRows(data.skills);
  const expRows = getRows(data.experience);
  const eduRows = getRows(data.education);

  return (
    <article className="cv-template cv-template--ats">
      <header className="cv-ats-header">
        <div className="cv-ats-title-row">
          <h1>{getText(data.full_name, "Ho va ten")}</h1>
          <span className="cv-ats-chip">ATS CLEAN</span>
        </div>
        <p>{getText(data.headline, "Vi tri ung tuyen")}</p>
        <div className="cv-ats-contact">
          <span>{getText(data.email, "Email")}</span>
          <span>{getText(data.phone, "So dien thoai")}</span>
          <span>{getText(data.address, "Dia chi")}</span>
        </div>
      </header>

      <section className="cv-ats-meta-grid">
        <p>
          <strong>Ngay sinh:</strong> {getText(data.dob)}
        </p>
        <p>
          <strong>Gioi tinh:</strong> {getText(data.gender)}
        </p>
        <p>
          <strong>Kinh nghiem:</strong>{" "}
          {data.years_experience
            ? `${data.years_experience} nam`
            : "Chua cap nhat"}
        </p>
        <p>
          <strong>Muc luong:</strong> {getText(data.expected_salary)}
        </p>
        <p>
          <strong>Khu vuc:</strong> {getText(data.desired_location)}
        </p>
        <p>
          <strong>Chuc danh:</strong> {getText(data.current_title)}
        </p>
      </section>

      <AtsSection
        title="Muc tieu nghe nghiep"
        rows={getRows(data.summary)}
        fallback={getText(data.summary)}
      />
      <AtsSection
        title="Kinh nghiem lam viec"
        rows={expRows}
        fallback={getText(data.experience)}
      />
      <AtsSection
        title="Hoc van"
        rows={eduRows}
        fallback={getText(data.education)}
      />
      <AtsSection
        title="Ky nang"
        rows={skillRows}
        fallback={getText(data.skills)}
        compact
      />
    </article>
  );
}

function AtsSection({ title, rows, fallback, compact = false }) {
  return (
    <section
      className={
        compact ? "cv-ats-section cv-ats-section--compact" : "cv-ats-section"
      }
    >
      <h2>{title}</h2>
      {rows.length ? (
        <ul className="cv-ats-list">
          {rows.map((row, index) => (
            <li key={`${row}-${index}`}>{row}</li>
          ))}
        </ul>
      ) : (
        <p className="cv-pre-wrap">{fallback}</p>
      )}
    </section>
  );
}
