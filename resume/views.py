import json
import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from ats.services.ats_engine import analyze_resume
from ats.services.pdf_parser import extract_text_from_pdf


STOPWORDS = {
    "the", "and", "or", "is", "in", "a", "to", "for", "of", "with", "on", "at",
    "be", "are", "was", "were", "this", "that", "have", "has", "by", "as", "an",
    "it", "its", "we", "you", "your", "our", "will", "can", "may", "from", "into",
    "about", "up", "also", "but", "not", "they", "their", "which", "when", "who",
    "how", "using", "used", "use", "looking", "seeking", "preferred", "required",
    "requirements", "responsibilities", "experience", "candidate", "role", "job",
}

SKILL_LIBRARY = [
    "python", "java", "c++", "c", "sql", "html", "css", "javascript", "typescript",
    "react", "django", "flask", "node.js", "rest api", "restful api", "api",
    "docker", "kubernetes", "aws", "git", "github", "linux", "mysql", "postgresql",
    "mongodb", "sqlite", "pandas", "numpy", "scikit-learn", "machine learning",
    "deep learning", "data structures", "algorithms", "oop", "dbms",
    "operating systems", "computer networks", "system design", "ci/cd",
    "github actions", "postman", "wireshark", "bash", "agile", "bootstrap",
    "php", "laravel", "spring boot", "next.js", "tailwind", "redis",
]


def _normalize_text(text):
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def _normalize_token(token):
    token = token.lower().strip().replace("–", "-").replace("—", "-")
    token = token.replace("restful", "rest").replace("apis", "api").replace("api's", "api")
    token = token.replace("object oriented programming", "oop")
    token = re.sub(r"[^a-z0-9+#./-]+", "", token)
    for suffix in ("ing", "ed", "es", "s"):
        if len(token) > 5 and token.endswith(suffix):
            token = token[: -len(suffix)]
            break
    return token


def _tokenize(text):
    tokens = set()
    for raw in re.findall(r"[A-Za-z0-9+#./-]+", _normalize_text(text)):
        token = _normalize_token(raw)
        if token and token not in STOPWORDS:
            tokens.add(token)
    return tokens


def _extract_skill_phrases(job_description):
    normalized_jd = _normalize_text(job_description)
    phrases = []

    for skill in SKILL_LIBRARY:
        if skill in normalized_jd:
            phrases.append(skill)

    title_case_phrases = re.findall(r"\b(?:[A-Z][a-zA-Z0-9+#./-]*\s?){1,3}", job_description or "")
    for phrase in title_case_phrases:
        cleaned = phrase.strip().lower()
        if len(cleaned) > 2 and cleaned not in STOPWORDS and cleaned not in phrases:
            phrases.append(cleaned)

    return phrases[:20]


def ats_score(resume_text, job_description):
    resume_text = resume_text or ""
    job_description = job_description or ""
    resume_tokens = _tokenize(resume_text)
    jd_tokens = _tokenize(job_description)
    jd_phrases = _extract_skill_phrases(job_description)
    normalized_resume = _normalize_text(resume_text)

    token_matches = {token for token in jd_tokens if token in resume_tokens}
    phrase_matches = [phrase for phrase in jd_phrases if phrase in normalized_resume]
    missing_phrases = [phrase for phrase in jd_phrases if phrase not in phrase_matches]

    token_score = (len(token_matches) / len(jd_tokens)) if jd_tokens else 0
    phrase_score = (len(phrase_matches) / len(jd_phrases)) if jd_phrases else token_score
    score = round(((token_score * 0.4) + (phrase_score * 0.6)) * 100)

    suggestions = []
    if missing_phrases:
        suggestions.append(
            f"Add missing role keywords in skills or project bullets: {', '.join(missing_phrases[:5])}."
        )
    if "project" not in normalized_resume:
        suggestions.append("Add project bullets with measurable impact and tools used.")
    if "experience" not in normalized_resume and "intern" not in normalized_resume:
        suggestions.append("Add internship or practical experience wording if you have relevant work.")
    if score < 80:
        suggestions.append("Mirror exact job-description terminology for tools, frameworks, and responsibilities.")

    matched = list(dict.fromkeys(phrase_matches + sorted(token_matches)))[:15]
    missing = list(dict.fromkeys(missing_phrases))[:15]
    return score, missing, matched, suggestions[:4]


def _build_resume_context(request):
    full_name = request.POST.get("full_name", "")
    email = request.POST.get("email", "")
    phone = request.POST.get("phone", "")
    linkedin = request.POST.get("linkedin", "")
    github = request.POST.get("github", "")
    portfolio = request.POST.get("portfolio", "")
    summary = request.POST.get("summary", "")
    skills_programming = request.POST.get("skills_programming", "")
    skills_web = request.POST.get("skills_web", "")
    skills_backend = request.POST.get("skills_backend", "")
    skills_db = request.POST.get("skills_db", "")
    skills_tools = request.POST.get("skills_tools", "")
    skills_other = request.POST.get("skills_other", "")

    skills_list = []
    for label, value in [
        ("Languages", skills_programming),
        ("Web", skills_web),
        ("Backend", skills_backend),
        ("Database", skills_db),
        ("Tools", skills_tools),
        ("Concepts", skills_other),
    ]:
        if value:
            skills_list.append({"label": label, "value": value})

    project_titles = request.POST.getlist("project_title[]")
    project_techs = request.POST.getlist("project_tech[]")
    project_githubs = request.POST.getlist("project_github[]")
    project_descs = request.POST.getlist("project_desc[]")

    projects_list = []
    for i in range(len(project_titles)):
        if project_titles[i].strip():
            points = [p.strip() for p in project_descs[i].split("\n") if p.strip()] if i < len(project_descs) else []
            projects_list.append(
                {
                    "title": project_titles[i],
                    "tech": project_techs[i] if i < len(project_techs) else "",
                    "github": project_githubs[i] if i < len(project_githubs) else "",
                    "points": points,
                }
            )

    exp_roles = request.POST.getlist("exp_role[]")
    exp_durations = request.POST.getlist("exp_duration[]")
    exp_orgs = request.POST.getlist("exp_org[]")
    exp_locations = request.POST.getlist("exp_location[]")
    exp_descs = request.POST.getlist("exp_desc[]")

    experience_list = []
    for i in range(len(exp_roles)):
        if exp_roles[i].strip():
            points = [p.strip() for p in exp_descs[i].split("\n") if p.strip()] if i < len(exp_descs) else []
            experience_list.append(
                {
                    "role": exp_roles[i],
                    "duration": exp_durations[i] if i < len(exp_durations) else "",
                    "org": exp_orgs[i] if i < len(exp_orgs) else "",
                    "location": exp_locations[i] if i < len(exp_locations) else "",
                    "points": points,
                }
            )

    edu_degrees = request.POST.getlist("edu_degree[]")
    edu_years = request.POST.getlist("edu_year[]")
    edu_colleges = request.POST.getlist("edu_college[]")
    edu_grades = request.POST.getlist("edu_grade[]")

    education_list = []
    for i in range(len(edu_degrees)):
        if edu_degrees[i].strip():
            education_list.append(
                {
                    "degree": edu_degrees[i],
                    "year": edu_years[i] if i < len(edu_years) else "",
                    "college": edu_colleges[i] if i < len(edu_colleges) else "",
                    "grade": edu_grades[i] if i < len(edu_grades) else "",
                }
            )

    return {
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github,
        "portfolio": portfolio,
        "summary": summary,
        "skills_programming": skills_programming,
        "skills_web": skills_web,
        "skills_backend": skills_backend,
        "skills_db": skills_db,
        "skills_tools": skills_tools,
        "skills_other": skills_other,
        "skills_list": skills_list,
        "projects_list": projects_list,
        "experience_list": experience_list,
        "education_list": education_list,
        "projects_json": json.dumps(projects_list),
        "experience_json": json.dumps(experience_list),
        "education_json": json.dumps(education_list),
    }


@login_required
def resume_home(request):
    context = {}
    if request.method == "POST":
        context = _build_resume_context(request)
        context["submitted"] = True
    return render(request, "resume/resume.html", context)


@login_required
def download_pdf(request):
    if request.method == "POST":
        from django.template.loader import render_to_string
        from weasyprint import HTML

        data = _build_resume_context(request)
        context = {
            "full_name": data["full_name"],
            "email": data["email"],
            "phone": data["phone"],
            "linkedin": data["linkedin"],
            "github": data["github"],
            "portfolio": data["portfolio"],
            "summary": data["summary"],
            "skills": bool(data["skills_list"]),
            "skills_list": data["skills_list"],
            "projects": bool(data["projects_list"]),
            "projects_list": data["projects_list"],
            "experience": bool(data["experience_list"]),
            "experience_list": data["experience_list"],
            "education": bool(data["education_list"]),
            "education_list": data["education_list"],
        }

        html_string = render_to_string("resume/resume_pdf.html", context)
        pdf = HTML(string=html_string).write_pdf()

        safe_name = re.sub(r"[^\w\s-]", "", data["full_name"]).strip().replace(" ", "_") or "resume"
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{safe_name}_Resume.pdf"'
        return response

    return redirect("resume_home")


@login_required
def ats_analyzer(request):
    context = {}
    if request.method == "POST":
        job_description = request.POST.get("job_description", "")
        resume_file = request.FILES.get("resume_file")
        resume_text_input = request.POST.get("resume_text", "")
        extracted_text = None

        if resume_file:
            extracted_text = extract_text_from_pdf(resume_file)
            resume_text = extracted_text or resume_text_input
        else:
            resume_text = resume_text_input

        if resume_text and job_description:
            result = analyze_resume(resume_text, job_description)
            score = result["score"]
            missing = result["missing_keywords"]
            matched = result["matched_keywords"]
            suggestions = result["suggestions"]
            if score >= 70:
                score_color = "green"
                score_msg = "Strong match"
            elif score >= 40:
                score_color = "amber"
                score_msg = "Moderate match - improve keywords"
            else:
                score_color = "red"
                score_msg = "Weak match - add missing keywords"

            context = {
                "score": score,
                "cosine_score": result.get("cosine_score", 0),
                "keyword_score": result.get("keyword_score", 0),
                "section_scores": result.get("section_scores", {}),
                "score_color": score_color,
                "score_msg": score_msg,
                "missing": missing,
                "matched": matched,
                "suggestions": suggestions,
                "highlighted_resume": result.get("highlighted_resume", ""),
                "eligibility": result.get("eligibility", {}),
                "debug": result.get("debug", {}),
                "job_description": job_description,
                "resume_text": resume_text_input,
                "uploaded_file_name": getattr(resume_file, "name", ""),
                "analyzed": True,
            }
        else:
            if resume_file and not extracted_text and not resume_text_input.strip():
                error_message = (
                    "Could not read text from this PDF. Please upload a text-based PDF or paste resume content manually."
                )
            elif not job_description.strip():
                error_message = "Please add the job description."
            else:
                error_message = "Please provide resume content by uploading a readable PDF or pasting resume text."

            context = {
                "error": error_message,
                "job_description": job_description,
                "resume_text": resume_text_input,
                "uploaded_file_name": getattr(resume_file, "name", ""),
            }

    return render(request, "resume/ats.html", context)
