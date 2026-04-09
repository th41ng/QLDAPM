import { useMemo, useRef } from "react";

export default function ResumeHeader({ onCreate, onUpload }) {
  const uploadRef = useRef(null);
  const quickActions = useMemo(
    () => [
      { label: "ATS-friendly", value: "Ưu tiên bố cục gọn" },
      { label: "Xuất PDF", value: "Dùng ngay khi ứng tuyển" },
    ],
    [],
  );

  return (
    <section className="landing-section panel rounded-[28px] border border-slate-200 bg-white p-6 shadow-[0_18px_40px_rgba(15,23,42,0.06)] md:p-7">
      <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
        <div className="max-w-3xl">
          <span className="eyebrow">Resume Workspace</span>
          <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950 md:text-4xl">CV của bạn</h1>
          <p className="mt-3 text-sm leading-7 text-slate-600 md:text-base">
            Tạo mới, tải lên và quản lý tất cả CV ở một nơi. Tập trung vào thao tác nhanh, dễ xem lại và sẵn sàng dùng khi ứng tuyển.
          </p>
          <div className="mt-5 flex flex-wrap gap-3">
            {quickActions.map((item) => (
              <div key={item.label} className="rounded-full border border-blue-100 bg-blue-50 px-4 py-2 text-sm text-blue-700">
                <strong className="font-semibold">{item.label}</strong>
                <span className="ml-2 text-blue-600/80">{item.value}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="flex flex-wrap gap-3 lg:justify-end">
          <button type="button" className="btn rounded-2xl px-5 py-3 text-sm font-semibold shadow-none" onClick={onCreate}>
            Tạo CV mới
          </button>
          <button
            type="button"
            className="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-blue-200 hover:text-blue-700"
            onClick={() => {
              onUpload?.();
              uploadRef.current?.click();
            }}
          >
            Upload CV
          </button>
          <input ref={uploadRef} type="file" accept=".pdf,.doc,.docx" className="hidden" onChange={(event) => onUpload?.(event.target.files?.[0] || null)} />
        </div>
      </div>
    </section>
  );
}