function formatDate(value) {
  if (!value) return "Chưa cập nhật";
  try {
    return new Date(value).toLocaleDateString("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  } catch {
    return "Chưa cập nhật";
  }
}

function getStatus(resume) {
  if (resume.is_primary) return { label: "Đang dùng", className: "bg-blue-50 text-blue-700 border-blue-100" };
  if (resume.source_type === "upload") return { label: "Đã upload", className: "bg-emerald-50 text-emerald-700 border-emerald-100" };
  return { label: "Sẵn sàng", className: "bg-slate-100 text-slate-700 border-slate-200" };
}

export default function ResumeList({ resumes, onView, onEdit, onDelete, exportUrl }) {
  return (
    <section className="rounded-[24px] border border-slate-200 bg-white p-5 shadow-[0_14px_30px_rgba(15,23,42,0.05)]">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div>
          <h3 className="text-lg font-semibold text-slate-900">Danh sách CV</h3>
          <p className="mt-1 text-sm text-slate-500">Quản lý toàn bộ CV tạo từ UI và CV tải lên trong cùng một nơi.</p>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">{resumes.length} CV</span>
      </div>

      <div className="grid gap-4">
        {resumes.length ? (
          resumes.map((resume) => {
            const status = getStatus(resume);
            return (
              <article key={resume.id} className="rounded-[22px] border border-slate-200 bg-slate-50 p-5 transition hover:border-blue-200 hover:bg-white hover:shadow-[0_16px_32px_rgba(29,78,216,0.08)]">
                <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                  <div className="min-w-0">
                    <div className="flex flex-wrap items-center gap-2">
                      <h4 className="text-lg font-semibold text-slate-900">{resume.title}</h4>
                      <span className={`rounded-full border px-2.5 py-1 text-xs font-semibold ${status.className}`}>{status.label}</span>
                      <span className="rounded-full border border-slate-200 bg-white px-2.5 py-1 text-xs font-medium text-slate-600">
                        {resume.source_type === "upload" ? "Upload" : "Tạo từ UI"}
                      </span>
                    </div>
                    <div className="mt-2 flex flex-wrap gap-x-5 gap-y-2 text-sm text-slate-500">
                      <span>Cập nhật: {formatDate(resume.updated_at)}</span>
                      <span>Mẫu: {resume.template_name || "Chưa chọn"}</span>
                      <span>Tag: {(resume.tags || []).length ? resume.tags.map((tag) => tag.name).join(", ") : "Chưa gắn tag"}</span>
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-2 lg:justify-end">
                    <button type="button" className="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-semibold text-slate-700 transition hover:border-blue-200 hover:text-blue-700" onClick={() => onView(resume)}>
                      Xem
                    </button>
                    <button type="button" className="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-semibold text-slate-700 transition hover:border-blue-200 hover:text-blue-700" onClick={() => onEdit(resume)}>
                      Sửa
                    </button>
                    <a className="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-semibold text-slate-700 transition hover:border-blue-200 hover:text-blue-700" href={exportUrl(resume.id, "pdf")} target="_blank" rel="noreferrer">
                      Tải xuống
                    </a>
                    <button type="button" className="rounded-xl border border-rose-200 bg-rose-50 px-3 py-2 text-sm font-semibold text-rose-700 transition hover:bg-rose-100" onClick={() => onDelete(resume)}>
                      Xóa
                    </button>
                  </div>
                </div>
              </article>
            );
          })
        ) : (
          <div className="rounded-[22px] border border-dashed border-slate-200 px-5 py-10 text-center text-sm text-slate-500">
            Chưa có CV nào. Hãy tạo CV mới hoặc upload một file CV sẵn có.
          </div>
        )}
      </div>
    </section>
  );
}