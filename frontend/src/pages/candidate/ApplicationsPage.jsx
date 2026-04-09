import { useEffect, useState } from "react";
import { api } from "../../api";

export default function CandidateApplicationsPage() {
  const [apps, setApps] = useState([]);

  useEffect(() => {
    api.applications.myApplications().then(setApps).catch(() => setApps([]));
  }, []);

  return (
    <section className="panel">
      <h1>Việc làm đã ứng tuyển</h1>
      <div className="grid">
        {apps.map((app) => (
          <article className="card" key={app.id}>
            <h3>{app.job?.title}</h3>
            <p className="muted">{app.job?.company?.company_name}</p>
            <p>Trạng thái: {app.status}</p>
            <p>CV: {app.resume?.title}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
