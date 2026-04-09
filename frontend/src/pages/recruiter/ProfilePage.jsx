import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { ROUTES } from "../../routes";

export default function RecruiterProfilePage() {
  const { user } = useAuth();

  return (
    <section className="dashboard-page">
      <div className="dashboard-hero">
        <div>
          <span className="eyebrow">Recruiter workspace</span>
          <h1>Hồ sơ tài khoản</h1>
          <p>Quản lý thông tin tài khoản và liên kết với công ty tuyển dụng.</p>
        </div>
      </div>

      <div className="profile-layout">
        <article className="dashboard-card">
          <div className="dashboard-card-head">
            <h2>Thông tin tài khoản</h2>
          </div>
          <div className="profile-summary">
            <div className="profile-avatar">{getInitials(user?.full_name || user?.email)}</div>
            <div>
              <strong>{user?.full_name || "Recruiter"}</strong>
              <p>{user?.email}</p>
              <span className="status-badge status-badge--open">{user?.role === "recruiter" ? "Nhà tuyển dụng" : "Tài khoản"}</span>
            </div>
          </div>

          <dl className="company-summary-list">
            <div>
              <dt>Vai trò</dt>
              <dd>{user?.role || "recruiter"}</dd>
            </div>
            <div>
              <dt>Trạng thái</dt>
              <dd>{user?.status || "active"}</dd>
            </div>
            <div>
              <dt>Phương thức gần nhất</dt>
              <dd>{formatAuthMethod(user?.auth_method_preference)}</dd>
            </div>
          </dl>
        </article>

        <aside className="dashboard-card dashboard-card--compact">
          <div className="dashboard-card-head">
            <h2>Điều hướng nhanh</h2>
          </div>
          <div className="shortcut-list">
            <Link className="dashboard-action-card dashboard-action-card--mini" to={ROUTES.recruiter.dashboard}>
              <strong>Về dashboard</strong>
              <span>Quay lại tổng quan tuyển dụng</span>
            </Link>
            <Link className="dashboard-action-card dashboard-action-card--mini" to={ROUTES.recruiter.company}>
              <strong>Chỉnh sửa công ty</strong>
              <span>Cập nhật hồ sơ doanh nghiệp</span>
            </Link>
            <Link className="dashboard-action-card dashboard-action-card--mini" to={ROUTES.recruiter.jobs}>
              <strong>Quản lý tin tuyển dụng</strong>
              <span>Xem và tạo các bài đăng mới</span>
            </Link>
          </div>
        </aside>
      </div>
    </section>
  );
}

function getInitials(name) {
  const raw = (name || "RJ").trim();
  return raw
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part.charAt(0))
    .join("")
    .toUpperCase();
}

function formatAuthMethod(method) {
  if (method === "otp") return "OTP";
  if (method === "password") return "Mật khẩu";
  return "Mật khẩu";
}
