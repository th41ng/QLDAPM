function getText(value, fallback = "Chua cap nhat") {
  const text = String(value ?? "")
    .replace(/\r\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
  return text || fallback;
}

function getList(value) {
  if (Array.isArray(value)) return value.filter(Boolean).map(String);
  return String(value ?? "")
    .split(/\n|,/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function getParagraphs(value) {
  return String(value ?? "")
    .replace(/\r\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .split(/\n{2,}/)
    .map((item) => item.trim())
    .filter(Boolean);
}

export default function ModernBlueTemplate({ data = {} }) {
  const skills = getList(data.skills);
  const expBlocks = getParagraphs(data.experience);
  const eduBlocks = getParagraphs(data.education);
  const contact = [
    { label: "Ngay sinh", value: data.dob },
    { label: "Gioi tinh", value: data.gender },
    { label: "So dien thoai", value: data.phone },
    { label: "Email", value: data.email },
    { label: "Dia chi", value: data.address },
  ];
  const goals = [
    { label: "Vi tri hien tai", value: data.current_title },
    {
      label: "So nam kinh nghiem",
      value: data.years_experience
        ? `${data.years_experience} nam`
        : "Chua cap nhat",
    },
    { label: "Muc luong mong muon", value: data.expected_salary },
    { label: "Khu vuc mong muon", value: data.desired_location },
  ];

  return (
    <article className="cv-template cv-template--modern-blue">
      <div className="cv-modern-topline">
        <span>Modern Blue</span>
        <span>{getText(data.current_title, "Candidate Profile")}</span>
      </div>

      <header className="cv-modern-header">
        <div className="cv-modern-avatar-wrap">
          <div className="cv-modern-avatar" aria-hidden="true" />
        </div>
        <div className="cv-modern-header-main">
          <h1>{getText(data.full_name, "Ho va ten")}</h1>
          <p className="cv-modern-headline">
            {getText(data.headline, "Vi tri ung tuyen")}
          </p>
          <div className="cv-modern-contact-grid">
            {contact.map((item) => (
              <p key={item.label}>
                <strong>{item.label}:</strong> {getText(item.value)}
              </p>
            ))}
          </div>

          <div className="cv-modern-chip-row">
            <span>{getText(data.expected_salary, "Luong thuong luong")}</span>
            <span>{getText(data.desired_location, "Linh hoat dia diem")}</span>
            <span>
              {data.years_experience
                ? `${data.years_experience} nam kinh nghiem`
                : "Dang cap nhat kinh nghiem"}
            </span>
          </div>
        </div>
      </header>

      <div className="cv-modern-grid">
        <aside className="cv-modern-aside">
          <h3>Muc tieu nghe nghiep</h3>
          <p className="cv-pre-wrap">{getText(data.summary)}</p>

          <h3>Thong tin bo sung</h3>
          <div className="cv-modern-meta-list">
            {goals.map((item) => (
              <p key={item.label}>
                <strong>{item.label}:</strong> {getText(item.value)}
              </p>
            ))}
          </div>

          <h3>Ky nang</h3>
          {skills.length ? (
            <ul className="cv-skill-list">
              {skills.map((skill) => (
                <li key={skill}>{skill}</li>
              ))}
            </ul>
          ) : (
            <p>Chua cap nhat</p>
          )}
        </aside>

        <section className="cv-modern-main">
          <section className="cv-modern-block">
            <h2>Kinh nghiem lam viec</h2>
            {expBlocks.length ? (
              <div className="cv-modern-stack">
                {expBlocks.map((block, index) => (
                  <article key={`${block}-${index}`} className="cv-modern-item">
                    <span className="cv-modern-item-dot" />
                    <p className="cv-pre-wrap">{block}</p>
                  </article>
                ))}
              </div>
            ) : (
              <p className="cv-pre-wrap">{getText(data.experience)}</p>
            )}
          </section>

          <section className="cv-modern-block">
            <h2>Hoc van</h2>
            {eduBlocks.length ? (
              <div className="cv-modern-stack">
                {eduBlocks.map((block, index) => (
                  <article key={`${block}-${index}`} className="cv-modern-item">
                    <span className="cv-modern-item-dot" />
                    <p className="cv-pre-wrap">{block}</p>
                  </article>
                ))}
              </div>
            ) : (
              <p className="cv-pre-wrap">{getText(data.education)}</p>
            )}
          </section>

          <section className="cv-modern-block">
            <h2>Thong tin them</h2>
            <p>
              CV duoc tao tu template Modern Blue. Ban co the tiep tuc cap nhat
              noi dung de phu hop voi vi tri ung tuyen.
            </p>
          </section>
        </section>
      </div>
    </article>
  );
}
