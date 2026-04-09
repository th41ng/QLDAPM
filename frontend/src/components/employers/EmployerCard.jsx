import { Link } from "react-router-dom";
import { ROUTES } from "../../routes";

export default function EmployerCard({ company, followed, onToggleFollow, onViewCompany }) {
  const logo = company.logo_url || company.logo || null;
  const name = company.company_name || company.name || "Nhà tuyển dụng";
  const rating = Number(company.rating || 4.5).toFixed(1);
  const matchScore = company.match_score || 80;
  const tags = Array.isArray(company.tags) ? company.tags.slice(0, 4) : [];
  const highlights = Array.isArray(company.hiring_focus) ? company.hiring_focus.slice(0, 2) : [];
  const viewCompanyProps = company.website
    ? { as: "a", href: company.website, target: "_blank", rel: "noreferrer" }
    : { as: Link, to: ROUTES.jobs };

  return (
    <article className="landing-employer-card panel-tile rounded-[24px] border border-slate-200/80 bg-gradient-to-b from-white to-slate-50 p-5 shadow-[0_14px_30px_rgba(29,78,216,0.08)] transition duration-200 hover:-translate-y-1 hover:border-blue-200 hover:shadow-[0_24px_44px_rgba(29,78,216,0.16)]">
      <div className="landing-employer-top flex items-start justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="employer-logo landing-employer-logo h-14 w-14 rounded-[18px] border border-slate-200 bg-white shadow-sm">
            {logo ? <img src={logo} alt={name} /> : <span className="text-sm font-extrabold tracking-[0.08em]">{getInitials(name)}</span>}
          </div>
          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <strong className="block truncate text-base font-semibold text-slate-900">{name}</strong>
              {company.badge ? (
                <span className="rounded-full bg-blue-50 px-2.5 py-1 text-[11px] font-semibold text-blue-700">{company.badge}</span>
              ) : null}
            </div>
            <p className="mt-1 text-sm text-slate-600">{company.industry || "Đang tuyển dụng"}</p>
          </div>
        </div>
        <div className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">{matchScore}% fit</div>
      </div>

      <div className="grid gap-3 rounded-[20px] border border-slate-200/80 bg-white/80 p-4 text-sm text-slate-600 sm:grid-cols-2">
        <Info label="Địa điểm" value={company.location || company.address || "Chưa cập nhật"} />
        <Info label="Quy mô" value={company.size || "50-100 nhân sự"} />
        <Info label="Đánh giá" value={`★ ${rating}/5`} />
        <Info label="Đang tuyển" value={`${company.openings ?? 0} vị trí`} />
      </div>

      {company.summary ? <p className="text-sm leading-6 text-slate-600">{company.summary}</p> : null}

      <div className="flex flex-wrap gap-2">
        {tags.map((tag) => (
          <span key={tag} className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-700">
            {tag}
          </span>
        ))}
        {highlights.map((tag) => (
          <span key={tag} className="rounded-full border border-blue-100 bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700">
            {tag}
          </span>
        ))}
      </div>

      <div className="landing-employer-foot mt-auto flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2 text-xs text-slate-500">
          <span className="employer-count rounded-full bg-blue-50 px-3 py-1.5 text-blue-700">{company.openings ?? 0} việc mở</span>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <Link className="btn rounded-xl px-4 py-2 text-sm shadow-none" to={ROUTES.jobs} onClick={() => onViewCompany(company)}>
            Xem việc làm
          </Link>
          <EmployerLink viewCompanyProps={viewCompanyProps} onClick={() => onViewCompany(company)} />
          <button
            type="button"
            onClick={() => onToggleFollow(company.id)}
            className={`rounded-xl border px-4 py-2 text-sm font-semibold transition ${
              followed ? "border-blue-200 bg-blue-50 text-blue-700" : "border-slate-200 bg-white text-slate-700 hover:border-blue-200 hover:text-blue-700"
            }`}
          >
            {followed ? "Đang theo dõi" : "Theo dõi"}
          </button>
        </div>
      </div>
    </article>
  );
}

function EmployerLink({ viewCompanyProps, onClick }) {
  if (viewCompanyProps.as === "a") {
    return (
      <a
        className="text-link inline-flex rounded-xl border border-transparent px-2 py-2 text-sm font-semibold text-slate-700 transition hover:text-blue-700"
        href={viewCompanyProps.href}
        target={viewCompanyProps.target}
        rel={viewCompanyProps.rel}
        onClick={onClick}
      >
        Xem công ty
      </a>
    );
  }

  return (
    <Link className="text-link inline-flex rounded-xl border border-transparent px-2 py-2 text-sm font-semibold text-slate-700 transition hover:text-blue-700" to={viewCompanyProps.to} onClick={onClick}>
      Xem công ty
    </Link>
  );
}

function Info({ label, value }) {
  return (
    <div className="grid gap-1">
      <span className="text-xs uppercase tracking-[0.14em] text-slate-400">{label}</span>
      <strong className="text-sm font-semibold text-slate-800">{value}</strong>
    </div>
  );
}

function getInitials(name) {
  return String(name || "JT")
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part.charAt(0))
    .join("")
    .toUpperCase();
}