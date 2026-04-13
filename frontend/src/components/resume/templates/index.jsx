import ATSCleanTemplate from "./ATSCleanTemplate";
import CreativeRoseTemplate from "./CreativeRoseTemplate";
import MinimalSlateTemplate from "./MinimalSlateTemplate";
import ModernBlueTemplate from "./ModernBlueTemplate";

function normalize(value) {
  return String(value ?? "")
    .toLowerCase()
    .trim()
    .replace(/\s+/g, "-");
}

const TEMPLATE_MAP = {
  "modern-blue": ModernBlueTemplate,
  "ats-clean": ATSCleanTemplate,
  "creative-minimal": CreativeRoseTemplate,
  "product-designer": CreativeRoseTemplate,
  "marketing-pro": CreativeRoseTemplate,
  "minimal-slate": MinimalSlateTemplate,
  "hr-executive": MinimalSlateTemplate,
  "data-analyst": MinimalSlateTemplate,
};

export function resolveTemplateComponent(slugOrName) {
  const key = normalize(slugOrName);
  if (TEMPLATE_MAP[key]) return TEMPLATE_MAP[key];
  if (key.includes("ats")) return ATSCleanTemplate;
  if (key.includes("creative") || key.includes("designer") || key.includes("marketing")) return CreativeRoseTemplate;
  if (key.includes("minimal") || key.includes("executive") || key.includes("analyst")) return MinimalSlateTemplate;
  return ModernBlueTemplate;
}
