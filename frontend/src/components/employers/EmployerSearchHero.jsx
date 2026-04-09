import EmployerFilterChips from "./EmployerFilterChips";

export default function EmployerSearchHero({ query, onQueryChange, quickFilters, activeFilter, onFilterChange, totalCompanies }) {
  return (
    <section className="landing-section panel relative overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,_rgba(59,130,246,0.18),_transparent_32%),radial-gradient(circle_at_bottom_left,_rgba(191,219,254,0.48),_transparent_34%)]" />
      <div className="relative grid gap-6 lg:grid-cols-[minmax(0,1.15fr)_320px] lg:items-start">
        <div>
          <span className="eyebrow">Khám phá công ty</span>
          <h1 className="mt-3 max-w-3xl text-3xl font-semibold tracking-tight text-slate-950 md:text-4xl">
            Khám phá nhà tuyển dụng phù hợp với bạn
          </h1>
          <p className="mt-3 max-w-2xl text-sm leading-7 text-slate-600 md:text-base">
            Tìm kiếm công ty theo ngành nghề, địa điểm và mức độ phù hợp với hồ sơ của bạn. Dữ liệu ưu tiên lấy từ hệ thống hiện có,
            sau đó làm giàu bằng gợi ý để ứng viên scan nhanh hơn.
          </p>

          <div className="mt-6 flex flex-col gap-3 rounded-[22px] border border-blue-100 bg-white/90 p-3 shadow-[0_18px_40px_rgba(29,78,216,0.08)] backdrop-blur md:flex-row md:items-center">
            <div className="flex min-w-0 flex-1 items-center gap-3 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
              <span className="text-lg text-slate-400">⌕</span>
              <input
                value={query}
                onChange={(event) => onQueryChange(event.target.value)}
                placeholder="Tìm theo tên công ty, ngành nghề, công nghệ hoặc địa điểm"
                className="w-full border-0 bg-transparent text-sm text-slate-900 outline-none placeholder:text-slate-400"
              />
            </div>
            <button type="button" className="btn min-w-[150px] rounded-2xl px-5 py-3 text-sm font-semibold shadow-none">
              Tìm công ty
            </button>
          </div>

          <EmployerFilterChips filters={quickFilters} activeFilter={activeFilter} onChange={onFilterChange} />
        </div>

        <aside className="grid gap-4">
          <div className="rounded-[24px] border border-white/70 bg-white/90 p-5 shadow-[0_20px_45px_rgba(15,23,42,0.08)]">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-blue-700">Tổng quan nhanh</p>
            <div className="mt-4 grid grid-cols-2 gap-3">
              <Metric label="Công ty" value={String(totalCompanies).padStart(2, "0")} />
              <Metric label="Đề xuất cao" value="06" />
              <Metric label="Remote" value="12" />
              <Metric label="Top fit" value="94%" />
            </div>
          </div>
          <div className="rounded-[24px] border border-blue-100 bg-gradient-to-br from-blue-50 to-white p-5 shadow-[0_18px_40px_rgba(29,78,216,0.08)]">
            <p className="text-sm font-semibold text-slate-900">Mẹo khám phá</p>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              Ưu tiên mở các công ty có độ phù hợp cao trước, sau đó lọc thêm theo địa điểm hoặc cấp độ tuyển dụng để danh sách gọn hơn.
            </p>
          </div>
        </aside>
      </div>
    </section>
  );
}

function Metric({ label, value }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
      <span className="block text-xs text-slate-500">{label}</span>
      <strong className="mt-1 block text-xl font-semibold text-blue-700">{value}</strong>
    </div>
  );
}