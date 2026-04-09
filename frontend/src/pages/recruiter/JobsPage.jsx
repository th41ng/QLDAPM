import { useEffect, useMemo, useState } from "react";
import { api } from "../../api";

const DEFAULT_FORM = {
  title: "",
  summary: "",
  description: "",
  responsibilities: "",
  requirements: "",
  location: "",
  status: "published",
};

const STATUS_OPTIONS = [
  { value: "all", label: "Tất cả" },
  { value: "draft", label: "Nháp" },
  { value: "published", label: "Đang đăng" },
  { value: "closed", label: "Đã đóng" },
];

export default function RecruiterJobsPage() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [query, setQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [locationFilter, setLocationFilter] = useState("all");
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [editingJobId, setEditingJobId] = useState(null);
  const [viewingJob, setViewingJob] = useState(null);
  const [form, setForm] = useState(DEFAULT_FORM);

  const loadJobs = async (status = statusFilter) => {
    setLoading(true);
    setError("");
    try {
      const suffix = status && status !== "all" ? `?status=${status}` : "";
      const data = await api.jobs.mine(suffix);
      setJobs(Array.isArray(data) ? data : []);
    } catch (loadError) {
      setJobs([]);
      setError(loadError.message || "Không thể tải danh sách bài tuyển dụng.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadJobs(statusFilter);
  }, [statusFilter]);

  const locationOptions = useMemo(() => {
    const values = [...new Set(jobs.map((job) => job.location).filter(Boolean))];
    return values.sort((left, right) => left.localeCompare(right, "vi"));
  }, [jobs]);

  const filteredJobs = useMemo(() => {
    const keyword = normalize(query);
    return jobs.filter((job) => {
      const haystack = normalize([job.title, job.summary, job.location, job.description].join(" "));
      const locationMatches = locationFilter === "all" || (job.location || "") === locationFilter;
      return (!keyword || haystack.includes(keyword)) && locationMatches;
    });
  }, [jobs, locationFilter, query]);

  const openCreateForm = () => {
    setEditingJobId(null);
    setForm(DEFAULT_FORM);
    setIsFormOpen(true);
  };

  const openEditForm = (job) => {
    setEditingJobId(job.id);
    setForm({
      title: job.title || "",
      summary: job.summary || "",
      description: job.description || "",
      responsibilities: job.responsibilities || "",
      requirements: job.requirements || "",
      location: job.location || "",
      status: job.status || "published",
    });
    setIsFormOpen(true);
  };

  const closeForm = () => {
    setIsFormOpen(false);
    setEditingJobId(null);
    setForm(DEFAULT_FORM);
  };

  const updateField = (field, value) => {
    setForm((current) => ({ ...current, [field]: value }));
  };

  const submitForm = async (statusOverride) => {
    const payload = {
      title: form.title.trim(),
      summary: form.summary.trim(),
      description: form.description.trim(),
      responsibilities: form.responsibilities.trim(),
      requirements: form.requirements.trim(),
      location: form.location.trim(),
      status: statusOverride || form.status,
    };

    try {
      setSubmitting(true);
      setMessage("");
      if (editingJobId) {
        await api.jobs.update(editingJobId, payload);
        setMessage("Đã cập nhật bài tuyển dụng.");
      } else {
        await api.jobs.create(payload);
        setMessage(payload.status === "draft" ? "Đã lưu bài tuyển dụng ở trạng thái nháp." : "Đã đăng bài tuyển dụng.");
      }
      closeForm();
      loadJobs(statusFilter);
    } catch (submitError) {
      setMessage(submitError.message || "Không thể lưu bài tuyển dụng.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (job) => {
    const confirmed = window.confirm(`Xóa bài tuyển dụng \"${job.title}\"?`);
    if (!confirmed) return;

    try {
      await api.jobs.delete(job.id);
      setMessage("Đã xóa bài tuyển dụng.");
      if (viewingJob?.id === job.id) setViewingJob(null);
      loadJobs(statusFilter);
    } catch (deleteError) {
      setMessage(deleteError.message || "Không thể xóa bài tuyển dụng.");
    }
  };

  const handleStatusChange = async (job, nextStatus) => {
    if (!nextStatus || nextStatus === job.status) return;
    try {
      await api.jobs.update(job.id, { status: nextStatus });
      setMessage("Đã cập nhật trạng thái bài tuyển dụng.");
      if (viewingJob?.id === job.id) {
        setViewingJob((current) => (current ? { ...current, status: nextStatus } : current));
      }
      loadJobs(statusFilter);
    } catch (statusError) {
      setMessage(statusError.message || "Không thể cập nhật trạng thái.");
    }
  };

  return (
    <div className="landing-page recruiter-jobs-page">
      <section className="landing-section panel rounded-[28px] border border-slate-200 bg-white p-6 shadow-[0_18px_40px_rgba(15,23,42,0.06)] md:p-7">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
          <div className="max-w-3xl">
            <span className="eyebrow">Recruiter workspace</span>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950 md:text-4xl">Quản lý bài tuyển dụng</h1>
            <p className="mt-3 text-sm leading-7 text-slate-600 md:text-base">
              Tạo, chỉnh sửa và theo dõi các bài đăng tuyển dụng của công ty. Giao diện ưu tiên thao tác nhanh, rõ trạng thái và dễ rà lại nội dung.
            </p>
          </div>
          <button type="button" className="btn rounded-2xl px-5 py-3 text-sm font-semibold shadow-none" onClick={openCreateForm}>
            + Đăng tuyển dụng
          </button>
        </div>
      </section>

      <section className="landing-section panel rounded-[26px] border border-slate-200 bg-white p-5 shadow-[0_16px_34px_rgba(15,23,42,0.05)]">
        <div className="grid gap-4 lg:grid-cols-[minmax(0,1.3fr)_220px_220px]">
          <label className="grid gap-2">
            <span className="text-sm font-semibold text-slate-700">Tìm theo tiêu đề</span>
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Nhập tiêu đề bài tuyển dụng"
              className="h-12 rounded-2xl border border-slate-200 bg-slate-50 px-4 text-sm text-slate-900 outline-none transition focus:border-blue-200 focus:bg-white"
            />
          </label>
          <label className="grid gap-2">
            <span className="text-sm font-semibold text-slate-700">Lọc theo location</span>
            <select
              value={locationFilter}
              onChange={(event) => setLocationFilter(event.target.value)}
              className="h-12 rounded-2xl border border-slate-200 bg-slate-50 px-4 text-sm text-slate-900 outline-none transition focus:border-blue-200 focus:bg-white"
            >
              <option value="all">Tất cả location</option>
              {locationOptions.map((location) => (
                <option key={location} value={location}>{location}</option>
              ))}
            </select>
          </label>
          <label className="grid gap-2">
            <span className="text-sm font-semibold text-slate-700">Lọc theo status</span>
            <select
              value={statusFilter}
              onChange={(event) => setStatusFilter(event.target.value)}
              className="h-12 rounded-2xl border border-slate-200 bg-slate-50 px-4 text-sm text-slate-900 outline-none transition focus:border-blue-200 focus:bg-white"
            >
              {STATUS_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </label>
        </div>
      </section>

      {message ? <div className="rounded-[20px] border border-blue-100 bg-blue-50 px-5 py-4 text-sm font-medium text-blue-700">{message}</div> : null}

      {loading ? <StateCard title="Đang tải bài tuyển dụng" description="Hệ thống đang lấy danh sách bài đăng của công ty." /> : null}
      {!loading && error ? <StateCard title="Không thể tải dữ liệu" description={error} tone="error" /> : null}
      {!loading && !error && !filteredJobs.length ? <StateCard title="Chưa có bài tuyển dụng phù hợp" description="Thử thay đổi bộ lọc hoặc tạo bài tuyển dụng mới để bắt đầu." tone="empty" /> : null}

      {!loading && !error && filteredJobs.length ? (
        <section className="grid gap-4 xl:grid-cols-2">
          {filteredJobs.map((job) => (
            <article key={job.id} className="rounded-[24px] border border-slate-200 bg-white p-5 shadow-[0_14px_30px_rgba(15,23,42,0.05)] transition hover:-translate-y-1 hover:border-blue-200 hover:shadow-[0_22px_40px_rgba(29,78,216,0.10)]">
              <div className="flex flex-col gap-4">
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <div className="flex flex-wrap items-center gap-2">
                      <h3 className="truncate text-xl font-semibold text-slate-900">{job.title || "Chưa có tiêu đề"}</h3>
                      <StatusBadge status={job.status} />
                    </div>
                    <p className="mt-2 text-sm leading-6 text-slate-600">{job.summary || "Chưa có tóm tắt cho bài tuyển dụng này."}</p>
                  </div>
                  <div className="shrink-0">
                    <select
                      value={job.status || "draft"}
                      onChange={(event) => handleStatusChange(job, event.target.value)}
                      className="h-10 rounded-xl border border-slate-200 bg-slate-50 px-3 text-sm text-slate-700 outline-none transition focus:border-blue-200 focus:bg-white"
                    >
                      {STATUS_OPTIONS.filter((option) => option.value !== "all").map((option) => (
                        <option key={option.value} value={option.value}>{option.label}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="grid gap-3 rounded-[20px] border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600 md:grid-cols-2">
                  <MetaItem label="Location" value={job.location || "Chưa cập nhật"} />
                  <MetaItem label="Tạo lúc" value={formatDate(job.created_at)} />
                  <MetaItem label="Cập nhật" value={formatDate(job.updated_at)} />
                  <MetaItem label="Trạng thái" value={mapStatusLabel(job.status)} />
                </div>

                <div className="flex flex-wrap gap-2">
                  <button type="button" className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-blue-200 hover:text-blue-700" onClick={() => setViewingJob(job)}>
                    Xem
                  </button>
                  <button type="button" className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-blue-200 hover:text-blue-700" onClick={() => openEditForm(job)}>
                    Sửa
                  </button>
                  <button type="button" className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-2 text-sm font-semibold text-rose-700 transition hover:bg-rose-100" onClick={() => handleDelete(job)}>
                    Xóa
                  </button>
                </div>
              </div>
            </article>
          ))}
        </section>
      ) : null}

      {isFormOpen ? (
        <JobFormModal
          form={form}
          editing={Boolean(editingJobId)}
          submitting={submitting}
          onClose={closeForm}
          onChange={updateField}
          onSubmit={() => submitForm()}
          onSaveDraft={() => submitForm("draft")}
        />
      ) : null}

      {viewingJob ? <JobDetailModal job={viewingJob} onClose={() => setViewingJob(null)} /> : null}
    </div>
  );
}

function JobFormModal({ form, editing, submitting, onClose, onChange, onSubmit, onSaveDraft }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4">
      <div className="max-h-[92vh] w-full max-w-4xl overflow-auto rounded-[28px] bg-white p-6 shadow-[0_32px_80px_rgba(15,23,42,0.24)] md:p-7">
        <div className="flex items-start justify-between gap-4 border-b border-slate-100 pb-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-blue-700">Recruiter editor</p>
            <h2 className="mt-2 text-2xl font-semibold text-slate-950">{editing ? "Chỉnh sửa bài tuyển dụng" : "Tạo bài tuyển dụng mới"}</h2>
            <p className="mt-1 text-sm text-slate-500">Chỉ dùng các trường đang có trong API hiện tại để tránh lệch dữ liệu backend.</p>
          </div>
          <button type="button" className="rounded-xl border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700" onClick={onClose}>
            Đóng
          </button>
        </div>

        <form
          className="mt-6 grid gap-5"
          onSubmit={(event) => {
            event.preventDefault();
            onSubmit();
          }}
        >
          <FormSection title="Thông tin cơ bản" description="Thiết lập tiêu đề, tóm tắt ngắn và location để bài đăng dễ scan hơn trong danh sách.">
            <div className="grid gap-4 md:grid-cols-2">
              <Field label="Title">
                <input value={form.title} onChange={(event) => onChange("title", event.target.value)} placeholder="Ví dụ: Frontend Developer" />
              </Field>
              <Field label="Location">
                <input value={form.location} onChange={(event) => onChange("location", event.target.value)} placeholder="TP. Hồ Chí Minh" />
              </Field>
              <Field label="Summary" full>
                <textarea rows="3" value={form.summary} onChange={(event) => onChange("summary", event.target.value)} placeholder="Mô tả ngắn về vị trí để hiển thị ở danh sách bài tuyển dụng" />
              </Field>
            </div>
          </FormSection>

          <FormSection title="Nội dung công việc" description="Tập trung vào mô tả công việc và trách nhiệm chính của vị trí đang tuyển.">
            <div className="grid gap-4">
              <Field label="Description">
                <textarea rows="6" value={form.description} onChange={(event) => onChange("description", event.target.value)} placeholder="Mô tả công việc chi tiết" />
              </Field>
              <Field label="Responsibilities">
                <textarea rows="5" value={form.responsibilities} onChange={(event) => onChange("responsibilities", event.target.value)} placeholder="Các đầu việc hoặc trách nhiệm chính" />
              </Field>
            </div>
          </FormSection>

          <FormSection title="Yêu cầu ứng viên" description="Chỉ điền các yêu cầu đang được backend hỗ trợ qua trường requirements.">
            <Field label="Requirements">
              <textarea rows="6" value={form.requirements} onChange={(event) => onChange("requirements", event.target.value)} placeholder="Yêu cầu kỹ năng, kinh nghiệm hoặc điều kiện ứng tuyển" />
            </Field>
          </FormSection>

          <div className="flex flex-wrap items-center justify-end gap-3">
            {!editing ? (
              <button type="button" className="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-blue-200 hover:text-blue-700" onClick={onSaveDraft}>
                Lưu nháp
              </button>
            ) : null}
            <button type="submit" className="btn rounded-2xl px-5 py-3 text-sm font-semibold shadow-none" disabled={submitting}>
              {submitting ? "Đang lưu..." : editing ? "Cập nhật" : "Đăng job"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function JobDetailModal({ job, onClose }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4">
      <div className="max-h-[92vh] w-full max-w-4xl overflow-auto rounded-[28px] bg-white p-6 shadow-[0_32px_80px_rgba(15,23,42,0.24)] md:p-7">
        <div className="flex items-start justify-between gap-4 border-b border-slate-100 pb-4">
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <h2 className="text-2xl font-semibold text-slate-950">{job.title}</h2>
              <StatusBadge status={job.status} />
            </div>
            <p className="mt-2 text-sm text-slate-500">{job.location || "Chưa cập nhật location"}</p>
          </div>
          <button type="button" className="rounded-xl border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700" onClick={onClose}>
            Đóng
          </button>
        </div>

        <div className="mt-6 grid gap-5">
          <DetailSection title="Summary" content={job.summary} />
          <DetailSection title="Description" content={job.description} />
          <DetailSection title="Responsibilities" content={job.responsibilities} />
          <DetailSection title="Requirements" content={job.requirements} />
          <section className="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
            <h3 className="text-base font-semibold text-slate-900">Thông tin hệ thống</h3>
            <div className="mt-3 grid gap-3 text-sm text-slate-600 md:grid-cols-2">
              <MetaItem label="Location" value={job.location || "Chưa cập nhật"} />
              <MetaItem label="Status" value={mapStatusLabel(job.status)} />
              <MetaItem label="Tạo lúc" value={formatDate(job.created_at)} />
              <MetaItem label="Cập nhật" value={formatDate(job.updated_at)} />
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}

function FormSection({ title, description, children }) {
  return (
    <section className="rounded-[24px] border border-slate-200 bg-white p-5 shadow-[0_14px_30px_rgba(15,23,42,0.05)]">
      <div className="mb-4 border-b border-slate-100 pb-4">
        <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
        <p className="mt-1 text-sm leading-6 text-slate-500">{description}</p>
      </div>
      {children}
    </section>
  );
}

function DetailSection({ title, content }) {
  return (
    <section className="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
      <h3 className="text-base font-semibold text-slate-900">{title}</h3>
      <p className="mt-3 whitespace-pre-wrap text-sm leading-7 text-slate-600">{content || "Chưa có nội dung"}</p>
    </section>
  );
}

function Field({ label, children, full }) {
  return (
    <label className={`grid gap-2 ${full ? "md:col-span-2" : ""}`}>
      <span className="text-sm font-semibold text-slate-700">{label}</span>
      {children}
    </label>
  );
}

function MetaItem({ label, value }) {
  return (
    <div className="grid gap-1">
      <span className="text-xs uppercase tracking-[0.14em] text-slate-400">{label}</span>
      <strong className="text-sm font-semibold text-slate-800">{value}</strong>
    </div>
  );
}

function StateCard({ title, description, tone = "default" }) {
  const toneClass =
    tone === "error"
      ? "border-rose-200 bg-rose-50 text-rose-700"
      : tone === "empty"
        ? "border-slate-200 bg-slate-50 text-slate-600"
        : "border-blue-100 bg-blue-50 text-blue-700";

  return (
    <section className={`rounded-[24px] border px-5 py-8 shadow-[0_14px_30px_rgba(15,23,42,0.04)] ${toneClass}`}>
      <h3 className="text-lg font-semibold">{title}</h3>
      <p className="mt-2 text-sm leading-6">{description}</p>
    </section>
  );
}

function StatusBadge({ status }) {
  const config = {
    draft: "border-slate-200 bg-slate-100 text-slate-700",
    published: "border-emerald-200 bg-emerald-50 text-emerald-700",
    closed: "border-amber-200 bg-amber-50 text-amber-700",
  };

  return (
    <span className={`rounded-full border px-2.5 py-1 text-xs font-semibold ${config[status] || config.draft}`}>
      {mapStatusLabel(status)}
    </span>
  );
}

function mapStatusLabel(status) {
  if (status === "published") return "Đang đăng";
  if (status === "closed") return "Đã đóng";
  return "Nháp";
}

function formatDate(value) {
  if (!value) return "Chưa cập nhật";
  try {
    return new Date(value).toLocaleString("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return "Chưa cập nhật";
  }
}

function normalize(value) {
  return String(value || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .trim();
}