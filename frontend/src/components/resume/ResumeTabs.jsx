export default function ResumeTabs({ activeTab, onChange }) {
  const tabs = [
    { id: "list", label: "CV của tôi" },
    { id: "create", label: "Tạo CV" },
    { id: "templates", label: "Mẫu CV" },
  ];

  return (
    <div className="rounded-[24px] border border-slate-200 bg-white p-2 shadow-[0_12px_28px_rgba(15,23,42,0.05)]">
      <div className="flex flex-wrap gap-2">
        {tabs.map((tab) => {
          const active = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              type="button"
              onClick={() => onChange(tab.id)}
              className={`min-h-[44px] rounded-2xl px-4 py-2 text-sm font-semibold transition ${
                active
                  ? "bg-blue-600 text-white shadow-[0_10px_24px_rgba(37,99,235,0.22)]"
                  : "text-slate-600 hover:bg-blue-50 hover:text-blue-700"
              }`}
            >
              {tab.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}