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

export default function ResumeUploadCard({ file, uploads, onPickFile, onSubmitUpload, busy }) {
  return (
    <div className="grid gap-4">
      <section className="rounded-[24px] border border-slate-200 bg-white p-5 shadow-[0_14px_30px_rgba(15,23,42,0.05)]">
        <div className="rounded-[22px] border-2 border-dashed border-blue-200 bg-blue-50/60 p-6 text-center">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-white text-2xl shadow-sm">↑</div>
          <h3 className="mt-4 text-lg font-semibold text-slate-900">Upload CV có sẵn</h3>
          <p className="mt-2 text-sm leading-6 text-slate-600">Kéo thả file vào đây hoặc chọn file từ máy của bạn. Hệ thống hỗ trợ CV PDF, DOC và DOCX.</p>
          <div className="mt-4 flex flex-wrap justify-center gap-2 text-xs font-medium text-slate-500">
            <span className="rounded-full bg-white px-3 py-1">PDF</span>
            <span className="rounded-full bg-white px-3 py-1">DOC</span>
            <span className="rounded-full bg-white px-3 py-1">DOCX</span>
          </div>
          <div className="mt-5 flex flex-col items-center gap-3 sm:flex-row sm:justify-center">
            <label className="cursor-pointer rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-blue-200 hover:text-blue-700">
              Chọn file
              <input type="file" accept=".pdf,.doc,.docx" className="hidden" onChange={(event) => onPickFile(event.target.files?.[0] || null)} />
            </label>
            <button type="button" className="btn rounded-2xl px-4 py-2 text-sm font-semibold shadow-none" onClick={onSubmitUpload} disabled={!file || busy}>
              {busy ? "Đang upload..." : "Upload CV"}
            </button>
          </div>
          <p className="mt-3 text-sm text-slate-500">{file ? `Đã chọn: ${file.name}` : "Chưa chọn file nào"}</p>
        </div>
      </section>

      <section className="rounded-[24px] border border-slate-200 bg-white p-5 shadow-[0_14px_30px_rgba(15,23,42,0.05)]">
        <div className="flex items-center justify-between gap-3">
          <h3 className="text-base font-semibold text-slate-900">Upload gần đây</h3>
          <span className="text-xs font-medium text-slate-500">{uploads.length} file</span>
        </div>
        <div className="mt-4 grid gap-3">
          {uploads.length ? (
            uploads.map((resume) => (
              <div key={resume.id} className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
                <strong className="block text-sm font-semibold text-slate-900">{resume.title}</strong>
                <div className="mt-1 flex items-center justify-between gap-3 text-xs text-slate-500">
                  <span>{resume.original_filename || resume.file_ext || "CV upload"}</span>
                  <span>{formatDate(resume.updated_at)}</span>
                </div>
              </div>
            ))
          ) : (
            <p className="rounded-2xl border border-dashed border-slate-200 px-4 py-5 text-sm text-slate-500">Chưa có file upload gần đây.</p>
          )}
        </div>
      </section>

      <section className="rounded-[24px] border border-blue-100 bg-gradient-to-br from-blue-50 to-white p-5 shadow-[0_14px_30px_rgba(29,78,216,0.08)]">
        <h3 className="text-base font-semibold text-slate-900">Mẹo tạo CV</h3>
        <ul className="mt-3 list-disc space-y-2 pl-5 text-sm leading-6 text-slate-600">
          <li>Đặt tiêu đề CV theo vị trí bạn muốn ứng tuyển để dễ quản lý.</li>
          <li>Headline nên ngắn, rõ năng lực chính và số năm kinh nghiệm.</li>
          <li>Dùng một CV chính làm bản đang ứng tuyển để thao tác nhanh ở các job detail.</li>
        </ul>
      </section>
    </div>
  );
}