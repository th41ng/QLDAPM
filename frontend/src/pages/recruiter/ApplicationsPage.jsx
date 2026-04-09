import { useEffect, useState } from "react";
import { api } from "../../api";

export default function RecruiterApplicationsPage() {
  const [apps, setApps] = useState([]);

  const load = () => api.applications.recruiterApplications().then(setApps).catch(() => setApps([]));
  useEffect(() => { load(); }, []);

  const updateStatus = async (id, status) => {
    await api.applications.updateStatus(id, status);
    load();
  };

  return (
    <section className="panel">
      <h1>Hồ sơ ứng tuyển</h1>
      <div className="grid">
        {apps.map((app) => (
          <article className="card" key={app.id}>
            <h3>{app.candidate?.full_name}</h3>
            <p className="muted">{app.job?.title}</p>
            <p>Resume: {app.resume?.title}</p>
            <div className="button-row">
              {["reviewing", "interview", "accepted", "rejected"].map((status) => (
                <button key={status} className="btn small" type="button" onClick={() => updateStatus(app.id, status)}>
                  {status}
                </button>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
