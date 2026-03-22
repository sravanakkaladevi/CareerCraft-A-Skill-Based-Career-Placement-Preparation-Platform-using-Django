import html
import logging
import re
from functools import lru_cache

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

TECH_KEYWORD_LIBRARY = {
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "sql",
    "html",
    "css",
    "react",
    "django",
    "flask",
    "node.js",
    "rest api",
    "rest apis",
    "api",
    "backend",
    "frontend",
    "web development",
    "database",
    "databases",
    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",
    "git",
    "github",
    "debugging",
    "testing",
    "software development lifecycle",
    "data structures",
    "algorithms",
    "problem solving",
    "scalability",
    "performance",
    "service",
    "services",
    "project",
    "projects",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "microservices",
    "distributed systems",
    "architecture",
    "security",
    "authentication",
    "data protection",
    "cloud",
    "cloud deployment",
    "ci/cd",
    "automated testing",
    "code review",
    "leadership",
    "mentoring",
    "mentor",
    "monitoring systems",
    "analytics tools",
    "ai/ml",
}

IMPORTANT_KEYWORD_WEIGHTS = {
    "python": 3,
    "java": 3,
    "javascript": 3,
    "django": 3,
    "react": 3,
    "backend": 3,
    "frontend": 3,
    "rest api": 4,
    "api": 3,
    "debugging": 3,
    "mysql": 3,
    "postgresql": 3,
    "database": 3,
    "git": 2,
    "data structures": 3,
    "algorithms": 3,
    "software development lifecycle": 3,
    "performance": 2,
    "scalability": 2,
    "aws": 3,
    "azure": 3,
    "gcp": 3,
    "docker": 3,
    "kubernetes": 3,
    "microservices": 3,
    "distributed systems": 3,
    "architecture": 3,
    "security": 3,
    "authentication": 2,
    "data protection": 2,
    "cloud": 2,
    "cloud deployment": 3,
    "ci/cd": 3,
    "automated testing": 2,
    "code review": 2,
    "leadership": 3,
    "mentoring": 2,
    "mentor": 2,
}

SECTION_WEIGHTS = {
    "skills": 0.4,
    "experience": 0.4,
    "projects": 0.2,
}

SECTION_HEADINGS = {
    "skills": ["skills", "technical skills", "tech stack", "technologies"],
    "projects": ["projects", "project", "academic projects", "personal projects"],
    "experience": ["experience", "work experience", "internship", "professional experience"],
}

SKILLS_SECTION_KEYWORDS = {
    "python", "java", "javascript", "typescript", "c", "c++", "sql", "html", "css",
    "react", "django", "flask", "node.js", "mysql", "postgresql", "mongodb", "sqlite",
    "git", "github", "database", "data structures", "algorithms", "aws", "azure", "gcp",
    "docker", "kubernetes", "cloud", "microservices", "distributed systems", "security",
    "authentication", "data protection", "ci/cd",
}
PROJECT_SECTION_KEYWORDS = {
    "api", "rest api", "backend", "frontend", "web development", "service", "project",
    "react", "django", "performance", "scalability", "microservices", "distributed systems",
    "cloud deployment", "aws", "azure", "gcp", "docker", "kubernetes",
}
EXPERIENCE_SECTION_KEYWORDS = {
    "debugging", "testing", "software development lifecycle", "performance", "scalability",
    "backend", "frontend", "service", "api", "rest api", "git", "architecture",
    "code review", "leadership", "mentoring", "mentor", "security", "ci/cd",
}
SECTION_KEYWORD_SETS = {
    "skills": SKILLS_SECTION_KEYWORDS,
    "experience": EXPERIENCE_SECTION_KEYWORDS,
    "projects": PROJECT_SECTION_KEYWORDS,
}

GENERIC_TERMS = {
    "need", "needs", "needed", "must", "should", "want", "wants", "looking", "seek",
    "candidate", "role", "job", "experience", "responsibility", "responsibilities",
    "requirement", "requirements", "preferred", "location", "duration", "month", "months",
    "intern", "internship", "work", "use", "assist", "help", "deliver", "understand",
    "understanding", "collaborate", "collaboration", "member", "members", "team",
    "maintain", "existing", "knowledge", "familiarity", "strong", "basic", "real",
    "world", "remote",
}

SYNONYM_MAP = {
    "apis": "api",
    "rest apis": "rest api",
    "restful api": "rest api",
    "restful apis": "rest api",
    "databases": "database",
    "services": "service",
    "projects": "project",
    "debug": "debugging",
    "tests": "testing",
    "node": "node.js",
    "lead": "leadership",
    "mentoring engineers": "mentoring",
    "mentor engineers": "mentoring",
    "code reviews": "code review",
    "cloud deployments": "cloud deployment",
}

MONTH_MAP = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}
LEADERSHIP_TERMS = {"leadership", "mentor", "mentoring", "code review", "architecture"}
SENIOR_JD_TERMS = {"leadership", "mentor", "mentoring", "code review", "architecture", "microservices", "distributed systems"}


@lru_cache(maxsize=1)
def get_nlp():
    try:
        return spacy.load("en_core_web_sm", disable=["ner"])
    except OSError:
        nlp = spacy.blank("en")
        if "lemmatizer" not in nlp.pipe_names:
            nlp.add_pipe("lemmatizer", config={"mode": "rule"})
        nlp.initialize()
        return nlp


def _normalize_keyword(value):
    value = re.sub(r"\s+", " ", (value or "").strip().lower())
    return SYNONYM_MAP.get(value, value)


def clean_latex(text):
    text = text or ""
    text = re.sub(r"\\[a-zA-Z]+(?:\*?)", " ", text)
    text = re.sub(r"\\.", " ", text)
    text = re.sub(r"\{[^{}]*\}", " ", text)
    text = text.replace("{", " ").replace("}", " ")
    return text


def clean_source_text(text):
    text = clean_latex(text or "")
    text = text.replace("Ã¢â‚¬â€œ", "-").replace("Ã¢â‚¬â€", "-")
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", " ", text)
    text = re.sub(r"[|â€¢â–ªâ—¦â—â– â—†]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def preprocess_text(text):
    cleaned_text = clean_source_text(text)
    if not cleaned_text:
        return [], ""

    doc = get_nlp()(cleaned_text.lower()[:50000])
    tokens = []
    for token in doc:
        if token.is_space or token.is_punct or token.is_stop:
            continue
        lemma = token.lemma_.strip().lower() if token.lemma_ and token.lemma_ != "-PRON-" else token.text.strip().lower()
        normalized = _normalize_keyword(lemma)
        if len(normalized) < 2 or normalized in GENERIC_TERMS:
            continue
        if token.pos_ and token.pos_ not in {"NOUN", "PROPN", "VERB", "ADJ"}:
            continue
        if not any(char.isalpha() for char in normalized):
            continue
        tokens.append(normalized)
    return list(dict.fromkeys(tokens)), " ".join(tokens)


def _extract_library_keywords(text):
    normalized_text = _normalize_keyword(clean_source_text(text))
    found = []
    for keyword in sorted(TECH_KEYWORD_LIBRARY, key=len, reverse=True):
        pattern = r"(?<![a-z0-9+#.])" + re.escape(keyword) + r"(?![a-z0-9+#.])"
        if re.search(pattern, normalized_text):
            found.append(_normalize_keyword(keyword))
    return found


def extract_keywords(text):
    cleaned_text = clean_source_text(text)
    if not cleaned_text:
        return []

    doc = get_nlp()(cleaned_text[:50000])
    keywords = _extract_library_keywords(cleaned_text)

    for chunk in getattr(doc, "noun_chunks", []):
        normalized = _normalize_keyword(chunk.text)
        if (
            normalized
            and 2 <= len(normalized) <= 40
            and normalized not in GENERIC_TERMS
            and any(char.isalpha() for char in normalized)
            and normalized in TECH_KEYWORD_LIBRARY
        ):
            keywords.append(normalized)

    for token in doc:
        if token.is_space or token.is_punct or token.is_stop:
            continue
        lemma = token.lemma_.strip().lower() if token.lemma_ and token.lemma_ != "-PRON-" else token.text.strip().lower()
        normalized = _normalize_keyword(lemma)
        if len(normalized) < 2 or normalized in GENERIC_TERMS:
            continue
        if token.pos_ and token.pos_ not in {"NOUN", "PROPN", "ADJ"}:
            continue
        if normalized in TECH_KEYWORD_LIBRARY:
            keywords.append(normalized)

    return list(dict.fromkeys(keywords))


def _keyword_weight(keyword):
    return IMPORTANT_KEYWORD_WEIGHTS.get(keyword, 1)


def _weighted_keyword_ratio(matched_keywords, jd_keywords):
    if not jd_keywords:
        return 0.0
    matched_weight = sum(_keyword_weight(keyword) for keyword in matched_keywords)
    total_weight = sum(_keyword_weight(keyword) for keyword in jd_keywords)
    return matched_weight / total_weight if total_weight else 0.0


def _build_weighted_similarity_document(document_keywords, jd_keywords, include_non_jd=True):
    jd_keyword_set = set(jd_keywords)
    parts = []
    for keyword in document_keywords:
        if keyword not in jd_keyword_set and not include_non_jd:
            continue
        if keyword not in jd_keyword_set and keyword in TECH_KEYWORD_LIBRARY and keyword not in IMPORTANT_KEYWORD_WEIGHTS:
            continue
        parts.extend([keyword] * _keyword_weight(keyword))
    return " ".join(parts)


def _score_keyword_block(document_text, jd_keywords, include_non_jd=True):
    document_keywords = extract_keywords(document_text)
    matched_keywords = sorted(set(document_keywords).intersection(jd_keywords))
    keyword_ratio = _weighted_keyword_ratio(matched_keywords, jd_keywords)

    similarity_doc = _build_weighted_similarity_document(document_keywords, jd_keywords, include_non_jd=include_non_jd)
    similarity_jd = _build_weighted_similarity_document(jd_keywords, jd_keywords)
    cosine_value = 0.0
    feature_names = []
    vector_shape = [0, 0]

    if similarity_doc and similarity_jd:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000, norm="l2")
        tfidf_matrix = vectorizer.fit_transform([similarity_doc, similarity_jd])
        cosine_value = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
        feature_names = vectorizer.get_feature_names_out().tolist()
        vector_shape = list(tfidf_matrix.shape)

    score = round(min(92.0, ((cosine_value * 0.7) + (keyword_ratio * 0.3)) * 100), 2)
    return {
        "score": score,
        "cosine_score": round(cosine_value, 4),
        "keyword_score": round(keyword_ratio, 4),
        "keywords": document_keywords,
        "matched_keywords": matched_keywords,
        "features": feature_names,
        "vector_shape": vector_shape,
    }


def split_sections(text):
    sections = {"skills": "", "projects": "", "experience": ""}
    current = None
    raw_lines = [line.strip() for line in clean_latex(text).splitlines()]

    for line in raw_lines:
        if not line:
            continue
        line_lower = line.lower()
        matched_heading = None
        for section, aliases in SECTION_HEADINGS.items():
            if any(alias == line_lower or alias in line_lower for alias in aliases):
                matched_heading = section
                break
        if matched_heading:
            current = matched_heading
            continue
        if current:
            sections[current] = f"{sections[current]} {line}".strip()

    cleaned_sections = {name: clean_source_text(value) for name, value in sections.items()}
    if not any(cleaned_sections.values()):
        full_resume = clean_source_text(text)
        return {"skills": full_resume, "projects": full_resume, "experience": full_resume}
    return cleaned_sections


def _suggest_section_for_keyword(keyword):
    if keyword in SKILLS_SECTION_KEYWORDS:
        return "skills"
    if keyword in EXPERIENCE_SECTION_KEYWORDS:
        return "experience"
    if keyword in PROJECT_SECTION_KEYWORDS:
        return "projects"
    return "skills"


def _section_keywords(jd_keywords, section_name):
    filtered = [keyword for keyword in jd_keywords if keyword in SECTION_KEYWORD_SETS.get(section_name, set())]
    return filtered or jd_keywords


def _keyword_span(keyword, css_class):
    return f"<span class=\"{css_class}\">{html.escape(keyword)}</span>"


def build_section_suggestions(missing_keywords):
    suggestions = {"skills": [], "experience": [], "projects": []}
    for keyword in missing_keywords[:12]:
        section = _suggest_section_for_keyword(keyword)
        suggestions[section].append(
            f"Add {_keyword_span(keyword, 'text-danger fw-semibold')} in your {section} section."
        )
    return suggestions


def highlight_keywords(text, keywords):
    cleaned_text = html.escape(clean_source_text(text))
    if not cleaned_text or not keywords:
        return cleaned_text
    unique_keywords = sorted(set(keywords), key=len, reverse=True)
    pattern = re.compile(
        r"(?<![a-zA-Z0-9+#.])(" + "|".join(re.escape(keyword) for keyword in unique_keywords) + r")(?![a-zA-Z0-9+#.])",
        flags=re.IGNORECASE,
    )
    return pattern.sub(lambda match: f"<span class=\"text-success fw-semibold\">{match.group(0)}</span>", cleaned_text)


def _log_debug_payload(raw_resume, clean_resume, raw_jd, clean_jd, feature_names, vector_shape, cosine_value):
    logger.debug("ATS raw resume text: %s", raw_resume[:1000])
    logger.debug("ATS cleaned resume text: %s", clean_resume[:1000])
    logger.debug("ATS raw job description text: %s", raw_jd[:1000])
    logger.debug("ATS cleaned job description text: %s", clean_jd[:1000])
    logger.debug("ATS TF-IDF feature names: %s", feature_names)
    logger.debug("ATS TF-IDF vector shape: %s", vector_shape)
    logger.debug("ATS cosine similarity: %s", cosine_value)


def extract_required_years(job_description):
    matches = re.findall(r"(\d+)\s*\+?\s*years?", job_description.lower())
    return max((int(value) for value in matches), default=0)


def _parse_month_year(token):
    token = token.strip().lower().replace("–", "-").replace("—", "-")
    parts = token.split()
    if len(parts) == 2 and parts[0] in MONTH_MAP and parts[1].isdigit():
        return int(parts[1]), MONTH_MAP[parts[0]]
    if len(parts) == 1 and parts[0].isdigit():
        return int(parts[0]), 1
    if token in {"present", "current"}:
        return None
    return None


def estimate_resume_experience_years(resume_text):
    cleaned = clean_source_text(resume_text)
    total_months = 0
    pattern = re.findall(
        r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}|\d{4})\s*[-–—]\s*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}|\d{4}|Present|Current)",
        cleaned,
        flags=re.IGNORECASE,
    )
    for start_raw, end_raw in pattern:
        start = _parse_month_year(start_raw)
        end = _parse_month_year(end_raw)
        if not start:
            continue
        start_year, start_month = start
        if end is None:
            continue
        end_year, end_month = end
        months = (end_year - start_year) * 12 + (end_month - start_month) + 1
        if months > 0:
            total_months += months
    return round(total_months / 12, 1)


def _leadership_gap(job_description, resume_keywords):
    jd_lower = job_description.lower()
    leadership_needed = any(term in jd_lower for term in {"lead", "mentor", "coach", "architecture", "code review", "leadership"})
    leadership_present = any(term in resume_keywords for term in LEADERSHIP_TERMS)
    return leadership_needed and not leadership_present


def build_eligibility(job_description, resume_text, score, matched_keywords, missing_keywords):
    required_years = extract_required_years(job_description)
    resume_years = estimate_resume_experience_years(resume_text)
    leadership_gap = _leadership_gap(job_description, matched_keywords)
    critical_missing = [kw for kw in missing_keywords if kw in {"aws", "azure", "gcp", "docker", "kubernetes", "microservices", "distributed systems", "architecture", "security", "ci/cd"}]

    reasons = []
    if required_years and resume_years < max(1, required_years - 1):
        reasons.append(f"JD asks for about {required_years}+ years, while the resume shows roughly {resume_years} years of dated experience.")
    if leadership_gap:
        reasons.append("The role expects lead-level ownership like architecture, mentoring, or code reviews, but that evidence is limited in the resume.")
    if critical_missing:
        reasons.append(f"Senior backend stack gaps still remain: {', '.join(critical_missing[:6])}.")

    if reasons:
        status = "Partially Eligible"
        summary = "Strong backend foundation, but this JD is asking for a more senior backend lead profile."
        if required_years >= 4 or leadership_gap:
            status = "Not Yet Eligible"
            summary = "Technical basics match, but the role level is above the current resume profile."
    elif score >= 70:
        status = "Eligible"
        summary = "The resume aligns well with the job level and technical expectations."
    else:
        status = "Partially Eligible"
        summary = "There is technical overlap, but the resume still needs clearer role-specific evidence."

    return {
        "status": status,
        "summary": summary,
        "required_years": required_years,
        "resume_years": resume_years,
        "reasons": reasons,
    }


def analyze_resume(resume_text, job_description):
    resume_text = resume_text or ""
    job_description = job_description or ""

    jd_keywords = extract_keywords(job_description)
    clean_resume = clean_source_text(resume_text)
    clean_jd = clean_source_text(job_description)

    if not resume_text.strip():
        empty_suggestions = {"skills": [], "experience": [], "projects": []}
        return {
            "score": 0,
            "section_scores": {"skills": 0, "experience": 0, "projects": 0},
            "matched_keywords": [],
            "missing_keywords": jd_keywords[:15],
            "highlighted_resume": "",
            "suggestions": empty_suggestions,
            "cosine_score": 0.0,
            "keyword_score": 0.0,
            "debug": {"clean_resume": "", "clean_jd": clean_jd, "features": [], "vector_shape": [0, 0]},
        }

    if not job_description.strip():
        empty_suggestions = {"skills": [], "experience": [], "projects": []}
        return {
            "score": 0,
            "section_scores": {"skills": 0, "experience": 0, "projects": 0},
            "matched_keywords": [],
            "missing_keywords": [],
            "highlighted_resume": html.escape(clean_resume),
            "suggestions": empty_suggestions,
            "cosine_score": 0.0,
            "keyword_score": 0.0,
            "debug": {"clean_resume": clean_resume, "clean_jd": "", "features": [], "vector_shape": [0, 0]},
        }

    global_score_data = _score_keyword_block(resume_text, jd_keywords)
    resume_keywords = global_score_data["keywords"]
    matched_keywords = global_score_data["matched_keywords"]
    missing_keywords = sorted(set(jd_keywords).difference(resume_keywords))

    resume_sections = split_sections(resume_text)
    section_scores = {}
    section_debug = {}
    for section_name in SECTION_WEIGHTS:
        section_jd_keywords = _section_keywords(jd_keywords, section_name)
        section_data = _score_keyword_block(
            resume_sections.get(section_name, ""),
            section_jd_keywords,
            include_non_jd=False,
        )
        section_scores[section_name] = round(section_data["score"])
        section_debug[section_name] = {
            "cosine_score": section_data["cosine_score"],
            "keyword_score": section_data["keyword_score"],
            "keywords": section_data["keywords"],
            "jd_keywords": section_jd_keywords,
        }

    weighted_section_score = sum(section_scores[name] * weight for name, weight in SECTION_WEIGHTS.items())
    final_score = min(92.0, round((weighted_section_score * 0.8) + (global_score_data["score"] * 0.2), 2))

    suggestions = build_section_suggestions(missing_keywords)
    highlighted_resume = highlight_keywords(resume_text, matched_keywords)
    eligibility = build_eligibility(job_description, resume_text, final_score, matched_keywords, missing_keywords)

    _log_debug_payload(
        raw_resume=resume_text,
        clean_resume=clean_resume,
        raw_jd=job_description,
        clean_jd=clean_jd,
        feature_names=global_score_data["features"],
        vector_shape=global_score_data["vector_shape"],
        cosine_value=global_score_data["cosine_score"],
    )

    return {
        "score": final_score,
        "section_scores": section_scores,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "highlighted_resume": highlighted_resume,
        "suggestions": suggestions,
        "eligibility": eligibility,
        "cosine_score": global_score_data["cosine_score"],
        "keyword_score": global_score_data["keyword_score"],
        "debug": {
            "clean_resume": clean_resume,
            "clean_jd": clean_jd,
            "features": global_score_data["features"],
            "vector_shape": global_score_data["vector_shape"],
            "sections": section_debug,
        },
    }
