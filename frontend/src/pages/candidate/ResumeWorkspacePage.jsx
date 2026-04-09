import { useEffect, useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { api } from "../../api";
import ResumeForm from "../../components/resume/ResumeForm";
import ResumeHeader from "../../components/resume/ResumeHeader";
import ResumeList from "../../components/resume/ResumeList";
import ResumeStats from "../../components/resume/ResumeStats";
import ResumeTabs from "../../components/resume/ResumeTabs";
import ResumeTemplateGrid from "../../components/resume/ResumeTemplateGrid";
import ResumeUploadCard from "../../components/resume/ResumeUploadCard";
import { cvTemplates } from "../../data/constants";
import { ROUTES } from "../../routes";

const EMPTY_FORM = {
  id: null,
  title: "CV mới",
  template_name: "Modern Blue",
  full_name: "",
  headline: "",
  summary: "",
  skills: "",
  experience: "",
  education: "",
  desired_location: "",
  years_experience: 0,
  is_primary: true,
};

export default function ResumeWorkspacePage({ defaultTab = "list" }) {
  const navigate = useNavigate();
  const location = useLocation();
  const [activeTab, setActiveTab] = useState(defaultTab);
  const [resumes, setResumes] = useState([]);
  const [message, setMessage] = useState("");
  const [manual, setManual] = useState(EMPTY_FORM);
  const [draftSavedAt, setDraftSavedAt] = useState("");
  const [previewResume, setPreviewResume] = useState(null);
  const [busy, setBusy] = useState(false);
  const [uploadFile, setUploadFile] = useState(null);

  const uploadedResumes = useMemo(() => resumes.filter((resume) => resume.source_type === "upload").slice(0, 4), [resumes]);

  const loadResumes = () => api.resumes.list().then(setResumes).catch(() => setResumes([]));

  useEffect(() => {
    loadResumes();
  }, []);

  useEffect(() => {
    setActiveTab(defaultTab);
  }, [defaultTab, location.pathname]);

  const setTab = (tab) => {
    setActiveTab(tab);
    if (tab === "templates") {
      navigate(ROUTES.candidate.templates);
      return;
    }
    navigate(ROUTES.candidate.resumes);
  };

  const handleChange = (field, value) => {
    setManual((current) => ({ ...current, [field]: value }));
  };

  const handleSaveDraft = () => {
    localStorage.setItem("candidate_resume_draft", JSON.stringify(manual));
    const timestamp = new Date().toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" });
    setDraftSavedAt(timestamp);
    setMessage(`Đã lưu nháp lúc ${timestamp}.`);
  };

  const handlePreview = () => {
    setPreviewResume({
      title: manual.title,
      structured_json: {
        full_name: manual.full_name,
        headline: manual.headline,
        summary: manual.summary,
        skills: manual.skills,
        experience: manual.experience,
        education: manual.education,
      },
      template_name: manual.template_name,
      source_type: "manual",
      is_primary: manual.is_primary,
    });
  };

  const handleSubmit = async () => {
    try {
      setBusy(true);
      const payload = {
        title: manual.title,
        template_name: manual.template_name,
        full_name: manual.full_name,
        headline: manual.headline,
        summary: manual.summary,
        skills: manual.skills,
        experience: manual.experience,
        education: manual.education,
        desired_location: manual.desired_location,
        years_experience: Number(manual.years_experience || 0),
        is_primary: manual.is_primary,
        structured_json: {
          full_name: manual.full_name,
          headline: manual.headline,
          summary: manual.summary,
          skills: manual.skills,
          experience: manual.experience,
          education: manual.education,
          desired_location: manual.desired_location,
          years_experience: Number(manual.years_experience || 0),
        },
        raw_text: JSON.stringify(manual),
      };

      if (manual.id) {
        await api.resumes.update(manual.id, payload);
        setMessage("Đã cập nhật CV.");
      } else {
        await api.resumes.createManual(payload);
        setMessage("Đã tạo CV mới.");
      }
      setManual(EMPTY_FORM);
      setActiveTab("list");
      navigate(ROUTES.candidate.resumes);
      loadResumes();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setBusy(false);
    }
  };

  const handleUpload = async (fileFromHeader) => {
    const file = fileFromHeader || uploadFile;
    if (!file) {
      setMessage("Chọn file trước khi upload.");
      return;
    }

    try {
      setBusy(true);
      const formData = new FormData();
      formData.append("file", file);
      formData.append("title", `CV upload - ${file.name}`);
      formData.append("is_primary", resumes.length ? "false" : "true");
      await api.resumes.upload(formData);
      setUploadFile(null);
      setMessage("Đã upload CV.");
      setActiveTab("list");
      navigate(ROUTES.candidate.resumes);
      loadResumes();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setBusy(false);
    }
  };

  const handleUseTemplate = (template) => {
    setManual((current) => ({ ...current, template_name: template.name, title: `${template.name} - CV mới` }));
    setActiveTab("create");
    navigate(ROUTES.candidate.resumes);
  };

  const handleEditResume = (resume) => {
    const structured = resume.structured_json || {};
    setManual({
      id: resume.id,
      title: resume.title || EMPTY_FORM.title,
      template_name: resume.template_name || "Modern Blue",
      full_name: structured.full_name || "",
      headline: structured.headline || "",
      summary: structured.summary || "",
      skills: structured.skills || "",
      experience: structured.experience || "",
      education: structured.education || "",
      desired_location: structured.desired_location || "",
      years_experience: structured.years_experience || 0,
      is_primary: Boolean(resume.is_primary),
    });
    setActiveTab("create");
    navigate(ROUTES.candidate.resumes);
  };

  const handleDeleteResume = async (resume) => {
    const confirmed = window.confirm(`Xóa CV \"${resume.title}\"?`);
    if (!confirmed) return;

    try {
      await api.resumes.remove(resume.id);
      setMessage("Đã xóa CV.");
      if (manual.id === resume.id) {
        setManual(EMPTY_FORM);
      }
      loadResumes();
    } catch (error) {
      setMessage(error.message);
    }
  };

  return (
    <div className="landing-page">
      <ResumeHeader
        onCreate={() => {
          setManual(EMPTY_FORM);
          setTab("create");
        }}
        onUpload={(file) => {
          if (file) {
            setUploadFile(file);
            handleUpload(file);
            return;
          }
          setTab("list");
        }}
      />

      <ResumeTabs activeTab={activeTab} onChange={setTab} />
      <ResumeStats resumes={resumes} />

      {message ? <div className="rounded-[20px] border border-blue-100 bg-blue-50 px-5 py-4 text-sm font-medium text-blue-700">{message}</div> : null}

      {(activeTab === "list" || activeTab === "create") ? (
        <div className="grid gap-5 xl:grid-cols-[360px_minmax(0,1fr)]">
          <ResumeUploadCard
            file={uploadFile}
            uploads={uploadedResumes}
            onPickFile={setUploadFile}
            onSubmitUpload={() => handleUpload()}
            busy={busy}
          />

          <div className="grid gap-5">
            {activeTab === "create" ? (
              <ResumeForm
                values={manual}
                onChange={handleChange}
                onSaveDraft={handleSaveDraft}
                onPreview={handlePreview}
                onSubmit={handleSubmit}
                saving={busy}
                editingTitle={manual.id ? "Chỉnh sửa CV" : undefined}
              />
            ) : null}

            <ResumeList
              resumes={resumes}
              onView={setPreviewResume}
              onEdit={handleEditResume}
              onDelete={handleDeleteResume}
              exportUrl={api.resumes.exportUrl}
            />
          </div>
        </div>
      ) : null}

      {activeTab === "templates" ? <ResumeTemplateGrid templates={cvTemplates} onUseTemplate={handleUseTemplate} /> : null}

      {draftSavedAt && activeTab === "create" ? (
        <div className="text-right text-sm text-slate-500">Nháp gần nhất: {draftSavedAt}</div>
      ) : null}

      {previewResume ? <PreviewModal resume={previewResume} onClose={() => setPreviewResume(null)} /> : null}
    </div>
  );
}

function PreviewModal({ resume, onClose }) {
  const structured = resume.structured_json || {};

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4">
      <div className="max-h-[90vh] w-full max-w-3xl overflow-auto rounded-[28px] bg-white p-6 shadow-[0_28px_80px_rgba(15,23,42,0.24)]">
        <div className="flex items-start justify-between gap-4 border-b border-slate-100 pb-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-700">Preview</p>
            <h3 className="mt-2 text-2xl font-semibold text-slate-950">{resume.title}</h3>
            <p className="mt-1 text-sm text-slate-500">Mẫu: {resume.template_name || "Chưa chọn"}</p>
          </div>
          <button type="button" className="rounded-xl border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700" onClick={onClose}>
            Đóng
          </button>
        </div>

        <div className="mt-6 grid gap-5">
          <PreviewSection title="Thông tin cơ bản">
            <p><strong>Họ tên:</strong> {structured.full_name || "Chưa cập nhật"}</p>
            <p><strong>Headline:</strong> {structured.headline || "Chưa cập nhật"}</p>
          </PreviewSection>
          <PreviewSection title="Summary" content={structured.summary} />
          <PreviewSection title="Skills" content={structured.skills} />
          <PreviewSection title="Experience" content={structured.experience} />
          <PreviewSection title="Education" content={structured.education} />
        </div>
      </div>
    </div>
  );
}

function PreviewSection({ title, children, content }) {
  return (
    <section className="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
      <h4 className="text-base font-semibold text-slate-900">{title}</h4>
      <div className="mt-3 space-y-2 whitespace-pre-wrap text-sm leading-7 text-slate-600">{children || content || "Chưa có nội dung"}</div>
    </section>
  );
}