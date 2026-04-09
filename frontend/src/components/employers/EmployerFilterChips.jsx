export default function EmployerFilterChips({ filters, activeFilter, onChange }) {
  return (
    <div className="filter-pills filter-pills--landing mt-5 flex flex-wrap gap-3">
      {filters.map((filter) => {
        const active = activeFilter === filter.value;
        return (
          <button
            key={filter.value}
            type="button"
            onClick={() => onChange(active ? "all" : filter.value)}
            className={`chip rounded-full border px-4 py-2 text-sm font-semibold transition-all duration-200 ${
              active
                ? "active-chip border-blue-600 bg-blue-600 text-white shadow-lg shadow-blue-100"
                : "border-slate-200 bg-white text-slate-700 hover:-translate-y-0.5 hover:border-blue-200 hover:bg-blue-50"
            }`}
          >
            {filter.label}
          </button>
        );
      })}
    </div>
  );
}