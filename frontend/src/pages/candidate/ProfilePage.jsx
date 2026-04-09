import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api";
import { ROUTES } from "../../routes";

const PROFILE_TABS = [
  { value: "profile", label: "Hồ sơ" },
  { value: "applications", label: "Việc đã ứng tuyển" },
];

const EMPTY_PROFILE = {
  dob: "",
  gender: "",
  address: "",
  headline: "",
  summary: "",
  current_title: "",
  years_experience: 0,
  expected_salary: "",
  desired_location: "",
  education: "",
  experience: "",
};

const EMPTY_APPLICATIONS = [];

export default function CandidateProfilePage() {
  const [activeTab, setActiveTab] = useState("profile");
  const [profile, setProfile] = useState(EMPTY_PROFILE);
  const [initialProfile, setInitialProfile] = useState(EMPTY_PROFILE);
  const [applications, setApplications] = useState(EMPTY_APPLICATIONS);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;

    const load = async () => {
      setLoading(true);
      try {
        const [profileData, applicationsData] = await Promise.all([
          api.resumes.getProfile().catch(() => null),
          api.applications.myApplications().catch(() => []),
        ]);

        if (!mounted) return;
        const nextProfile = normalizeProfile(profileData);
        setProfile(nextProfile);
        setInitialProfile(nextProfile);
        setApplications(Array.isArray(applicationsData) ? applicationsData : []);
      } finally {
        if (mounted) setLoading(false);
      }
    };

    load();

    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    if (!toast) return undefined;
    const timer = window.setTimeout(() => setToast(""), 2800);
    return () => window.clearTimeout(timer);
  }, [toast]);

  const stats = useMemo(
    () => [
      { label: "CV chính", value: "1" },
      { label: "Hồ sơ ứng tuyển", value: String(applications.length) },
      { label: "Kinh nghiệm", value: profile.years_experience ? `${profile.years_experience} năm` : "0 năm" },
    ],
    [applications.length, profile.years_experience],
  );

  const submit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      const payload = {
        ...profile,
        years_experience: Number(profile.years_experience) || 0,
      };
      const data = await api.resumes.updateProfile(payload);
      const nextProfile = normalizeProfile(data);
      setProfile(nextProfile);
      setInitialProfile(nextProfile);
      setToast("Đã lưu hồ sơ thành công.");
    } catch (err) {
      setError(err.message || "Không thể lưu hồ sơ.");
    } finally {
      setSaving(false);
    }
  };

  const resetProfile = () => {
    setProfile(initialProfile);
    setError("");
  };

  return (
    <section className="candidate-profile-page">
      <div className="candidate-page-head">
        <div>
          <span className="eyebrow">JOBPORTAL</span>
          <h1>Hồ sơ ứng viên</h1>
          <p>Cập nhật thông tin hồ sơ để nhà tuyển dụng dễ dàng tìm thấy bạn hơn.</p>
        </div>

        <div className="candidate-page-meta">
          {stats.map((item) => (
            <div key={item.label} className="candidate-meta-chip">
              <span>{item.label}</span>
              <strong>{item.value}</strong>
            </div>
          ))}
        </div>
      </div>

      <div className="candidate-profile-tabs" role="tablist" aria-label="Điều hướng hồ sơ ứng viên">
        {PROFILE_TABS.map((tab) => (
          <button
            key={tab.value}
            type="button"
            role="tab"
            aria-selected={activeTab === tab.value}
            className={activeTab === tab.value ? "candidate-tab candidate-tab--active" : "candidate-tab"}
            onClick={() => setActiveTab(tab.value)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <article className="candidate-profile-card">
        {activeTab === "profile" ? (
          <form className="candidate-form" onSubmit={submit} noValidate>
            {error ? <div className="auth-alert auth-alert--error">{error}</div> : null}
            <ProfileSection
              index="01"
              title="Thông tin cá nhân"
              description="Cập nhật dữ liệu cơ bản để hồ sơ của bạn rõ ràng và chuyên nghiệp hơn."
            >
              <div className="candidate-form-grid">
                <ProfileField
                  label="Ngày sinh"
                  input={
                    <input
                      type="date"
                      value={profile.dob || ""}
                      onChange={(event) => setProfile((prev) => ({ ...prev, dob: event.target.value }))}
                    />
                  }
                />
                <ProfileField
                  label="Giới tính"
                  input={
                    <select
                      value={profile.gender || ""}
                      onChange={(event) => setProfile((prev) => ({ ...prev, gender: event.target.value }))}
                    >
                      <option value="">Chọn giới tính</option>
                      <option value="male">Nam</option>
                      <option value="female">Nữ</option>
                      <option value="other">Khác</option>
                    </select>
                  }
                />
                <ProfileField
                  label="Địa chỉ"
                  input={
                    <input
                      value={profile.address || ""}
                      onChange={(event) => setProfile((prev) => ({ ...prev, address: event.target.value }))}
                      placeholder="Ví dụ: TP. Hồ Chí Minh"
                    />
                  }
                />
                <ProfileField
                  label="Headline"
                  input={
                    <input
                      value={profile.headline || ""}
                      onChange={(event) => setProfile((prev) => ({ ...prev, headline: event.target.value }))}
                      placeholder="Ví dụ: Frontend Developer / React"
                    />
                  }
                />
              </div>
            </ProfileSection>

            <ProfileSection
              index="02"
              title="Thông tin nghề nghiệp"
              description="Giúp nhà tuyển dụng nắm rõ định hướng công việc và mức độ kinh nghiệm của bạn."
            >
              <div className="candidate-form-grid">
                <ProfileField
                  label="Current title"
                  input={
                    <input
                      value={profile.current_title || ""}
                      onChange={(event) => setProfile((prev) => ({ ...prev, current_title: event.target.value }))}
                      placeholder="Ví dụ: Junior Web Developer"
                    />
                  }
                />
                <ProfileField
                  label="Years exp"
                  input={
                    <input
                      type="number"
                      min="0"
                      step="1"
                      value={profile.years_experience ?? 0}
                      onChange={(event) =>
                        setProfile((prev) => ({
                          ...prev,
                          years_experience: event.target.value === "" ? "" : Number(event.target.value),
                        }))
                      }
                      placeholder="0"
                    />
                  }
                />
                <ProfileField
                  label="Expected salary"
                  input={
                    <input
                      value={profile.expected_salary || ""}
                      onChange={(event) => setProfile((prev) => ({ ...prev, expected_salary: event.target.value }))}
                      placeholder="Ví dụ: 12 - 18 triệu"
                    />
                  }
                />
                <ProfileField
                  label="Desired location"
                  input={
                    <input
                      value={profile.desired_location || ""}
                      onChange={(event) => setProfile((prev) => ({ ...prev, desired_location: event.target.value }))}
                      placeholder="Ví dụ: TP. Hồ Chí Minh"
                    />
                  }
                />
              </div>
            </ProfileSection>

            <ProfileSection
              index="03"
              title="Hồ sơ chuyên môn"
              description="Mô tả ngắn gọn năng lực, học vấn và kinh nghiệm của bạn."
            >
              <div className="candidate-form-stack">
                <ProfileField
                  label="Summary"
                  fullWidth
                  input={
                    <textarea
                      rows="5"
                      value={profile.summary || ""}
                      onChange={(event) => setProfile((prev) => ({ ...prev, summary: event.target.value }))}
                      placeholder="Tóm tắt điểm mạnh, kỹ năng nổi bật và mục tiêu nghề nghiệp của bạn."
                    />
                  }
                />
                <ProfileField
                  label="Education"
                  fullWidth
                  input={
                    <textarea
                      rows="4"
                      value={profile.education || ""}
                      onChange={(event) => setProfile((prev) => ({ ...prev, education: event.target.value }))}
                      placeholder="Ví dụ: Đại học ... / Chuyên ngành / Bằng cấp / Chứng chỉ..."
                    />
                  }
                />
                <ProfileField
                  label="Experience"
                  fullWidth
                  input={
                    <textarea
                      rows="4"
                      value={profile.experience || ""}
                      onChange={(event) => setProfile((prev) => ({ ...prev, experience: event.target.value }))}
                      placeholder="Mô tả kinh nghiệm làm việc, dự án, thành tựu nổi bật..."
                    />
                  }
                />
              </div>
            </ProfileSection>

            <div className="candidate-form-actions">
              <button className="btn btn-ghost btn-small candidate-secondary-btn" type="button" onClick={resetProfile} disabled={saving || loading}>
                Đặt lại
              </button>
              <button className="btn candidate-primary-btn" type="submit" disabled={saving || loading}>
                {saving ? "Đang lưu..." : "Lưu hồ sơ"}
              </button>
            </div>
          </form>
        ) : (
          <div className="candidate-applications-panel">
            <div className="candidate-panel-head">
              <div>
                <h2>Việc đã ứng tuyển</h2>
                <p>Theo dõi trạng thái các hồ sơ đã nộp gần đây.</p>
              </div>
              <Link className="candidate-panel-link" to={ROUTES.jobs}>
                Xem việc làm
              </Link>
            </div>

            {loading ? (
              <div className="candidate-empty-state">Đang tải danh sách ứng tuyển...</div>
            ) : applications.length ? (
              <div className="candidate-application-list">
                {applications.map((application) => (
                  <article key={application.id} className="candidate-application-card">
                    <div className="candidate-application-main">
                      <div className="candidate-application-title">
                        <div>
                          <h3>{application.job?.title || "Tin tuyển dụng"}</h3>
                          <p>{application.job?.company?.company_name || "Nhà tuyển dụng"}</p>
                        </div>
                        <StatusBadge status={application.status} />
                      </div>
                      <div className="candidate-application-meta">
                        <span>{application.job?.location || "Chưa cập nhật địa điểm"}</span>
                        <span>{formatDate(application.applied_at)}</span>
                        <span>{application.resume?.title || "CV online"}</span>
                      </div>
                    </div>
                    <Link className="icon-btn" to={`/jobs/${application.job_id}`}>
                      Xem chi tiết
                    </Link>
                  </article>
                ))}
              </div>
            ) : (
              <div className="candidate-empty-state candidate-empty-state--large">
                <strong>Bạn chưa có hồ sơ ứng tuyển nào</strong>
                <p>Hãy khám phá các tin tuyển dụng phù hợp và nộp hồ sơ ngay hôm nay.</p>
                <Link className="btn btn-small" to={ROUTES.jobs}>
                  Khám phá việc làm
                </Link>
              </div>
            )}
          </div>
        )}
      </article>

      {toast ? <div className="candidate-toast" role="status">{toast}</div> : null}
    </section>
  );
}

function ProfileSection({ index, title, description, children }) {
  return (
    <section className="candidate-section">
      <div className="candidate-section-head">
        <div className="candidate-section-title">
          <span>{index}</span>
          <div>
            <h2>{title}</h2>
            <p>{description}</p>
          </div>
        </div>
      </div>
      {children}
    </section>
  );
}

function ProfileField({ label, input, fullWidth = false }) {
  return (
    <label className={fullWidth ? "candidate-field candidate-field--full" : "candidate-field"}>
      <span>{label}</span>
      {input}
    </label>
  );
}

function StatusBadge({ status }) {
  const normalized = (status || "").toLowerCase();
  const labelMap = {
    submitted: "Đã gửi",
    reviewing: "Đang xem xét",
    interview: "Phỏng vấn",
    accepted: "Đã chấp nhận",
    rejected: "Từ chối",
    withdrawn: "Đã rút",
  };
  const toneMap = {
    submitted: "new",
    reviewing: "reviewing",
    interview: "contacted",
    accepted: "open",
    rejected: "closed",
    withdrawn: "hidden",
  };

  return (
    <span className={`status-badge status-badge--${toneMap[normalized] || "hidden"}`}>
      {labelMap[normalized] || "Đã gửi"}
    </span>
  );
}

function normalizeProfile(profile) {
  return {
    ...EMPTY_PROFILE,
    ...(profile || {}),
    years_experience: profile?.years_experience ?? 0,
  };
}

function formatDate(value) {
  if (!value) return "Hôm nay";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Hôm nay";
  return new Intl.DateTimeFormat("vi-VN", { day: "2-digit", month: "2-digit", year: "numeric" }).format(date);
}
