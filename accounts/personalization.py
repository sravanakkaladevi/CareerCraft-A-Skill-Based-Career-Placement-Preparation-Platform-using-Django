from copy import deepcopy

from django.utils import timezone


ROLE_CHOICES = [
    ("frontend", "Frontend Developer"),
    ("backend", "Backend Developer"),
    ("fullstack", "Full Stack Developer"),
    ("data", "Data Analyst"),
    ("ai_ml", "AI / ML Engineer"),
    ("devops", "DevOps / Cloud Engineer"),
    ("cybersecurity", "Cybersecurity Analyst"),
    ("mobile", "Android Developer"),
]

DOMAIN_CHOICES = [
    ("web", "Web Development"),
    ("ai_ml", "AI / ML"),
    ("data_science", "Data Science"),
    ("cloud", "Cloud / DevOps"),
    ("cybersecurity", "Cybersecurity"),
    ("android", "Android"),
    ("careertech", "CareerTech"),
    ("edtech", "EdTech"),
]

EXPERIENCE_CHOICES = [
    ("fresher", "Fresher"),
    ("experienced", "Experienced"),
]

ROLE_DOMAIN_MAP = {
    "frontend": "web",
    "backend": "web",
    "fullstack": "web",
    "data": "data_science",
    "ai_ml": "ai_ml",
    "devops": "cloud",
    "cybersecurity": "cybersecurity",
    "mobile": "android",
}

DOMAIN_LANGUAGE_MAP = {
    "web": {"HTML", "JavaScript", "Python", "Django", "SQL", "MySQL"},
    "ai_ml": {"Python", "SQL"},
    "data_science": {"Python", "SQL", "MySQL"},
    "cloud": {"Python", "SQL", "Django"},
    "cybersecurity": {"Python", "SQL", "C Programming", "C++"},
    "android": {"Java", "Core Java", "Advanced Java", "SQL"},
    "careertech": {"Python", "Django", "JavaScript", "SQL", "MySQL"},
    "edtech": {"Python", "Django", "JavaScript", "SQL"},
}

DOMAIN_INTERVIEW_MAP = {
    "web": {"Python", "Web Dev", "Django", "DBMS", "Operating Systems", "Computer Networks", "OOPS", "Aptitude", "HR Questions"},
    "ai_ml": {"Python", "DSA", "DBMS", "Aptitude", "HR Questions"},
    "data_science": {"Python", "SQL", "DBMS", "Aptitude", "HR Questions"},
    "cloud": {"Python", "Django", "DBMS", "Operating Systems", "Computer Networks", "System Design", "Aptitude", "HR Questions"},
    "cybersecurity": {"Python", "Computer Networks", "Operating Systems", "DBMS", "Aptitude", "HR Questions"},
    "android": {"Core Java", "Java", "Advanced Java", "OOPS", "DBMS", "Aptitude", "HR Questions"},
    "careertech": {"Python", "Django", "Web Dev", "DBMS", "Aptitude", "HR Questions"},
    "edtech": {"Python", "Django", "Web Dev", "DBMS", "Aptitude", "HR Questions"},
}

PROFILE_SUMMARIES = {
    "frontend": "Focus on UI, JavaScript, and role-ready project practice.",
    "backend": "Focus on APIs, databases, and backend interview preparation.",
    "fullstack": "See balanced learning tracks for frontend, backend, and placement prep.",
    "data": "Focus on analytics, Python, SQL, and data-driven projects.",
    "ai_ml": "Focus on Python, ML foundations, and AI project portfolios.",
    "devops": "Focus on cloud, systems, architecture, and deployment skills.",
    "cybersecurity": "Focus on systems, networking, and security-oriented practice.",
    "mobile": "Focus on Java, Android, and mobile-friendly project ideas.",
}


def get_profile_setup_choices():
    return {
        "role_choices": ROLE_CHOICES,
        "experience_choices": EXPERIENCE_CHOICES,
    }


def apply_profile_inputs(profile, data):
    profile.target_role = (data.get("target_role") or "").strip()
    profile.target_domain = ROLE_DOMAIN_MAP.get(profile.target_role, "")
    profile.experience_level = (data.get("experience_level") or "fresher").strip() or "fresher"
    return profile


def queue_profile_change(profile, data):
    profile.pending_target_role = (data.get("target_role") or "").strip()
    profile.pending_target_domain = ROLE_DOMAIN_MAP.get(profile.pending_target_role, "")
    profile.pending_experience_level = (data.get("experience_level") or "fresher").strip() or "fresher"
    profile.role_change_requested_at = timezone.now()
    profile.role_change_reviewed_at = None
    profile.role_change_status = "pending"
    return profile


def approve_pending_profile_change(profile):
    if profile.pending_target_role:
        profile.target_role = profile.pending_target_role
    if profile.pending_target_domain:
        profile.target_domain = profile.pending_target_domain
    if profile.pending_experience_level:
        profile.experience_level = profile.pending_experience_level
    profile.role_change_status = "accepted"
    profile.role_change_reviewed_at = timezone.now()
    return profile


def clear_pending_profile_change(profile):
    profile.role_change_status = "rejected"
    profile.role_change_reviewed_at = timezone.now()
    return profile


def get_effective_domain(profile):
    if getattr(profile, "target_domain", ""):
        return profile.target_domain
    return ROLE_DOMAIN_MAP.get(getattr(profile, "target_role", ""), "")


def filter_languages_for_profile(languages, profile):
    domain = get_effective_domain(profile)
    allowed = DOMAIN_LANGUAGE_MAP.get(domain)
    if not allowed:
        return list(languages)
    filtered = [language for language in languages if language.name in allowed]
    return filtered or list(languages)


def filter_categories_for_profile(categories, profile):
    domain = get_effective_domain(profile)
    allowed = DOMAIN_INTERVIEW_MAP.get(domain)
    category_list = list(categories)
    if not allowed:
        return category_list

    filtered = []
    for category in category_list:
        if category.name in allowed:
            filtered.append(category)
            continue
        if category.name == "System Design" and getattr(profile, "experience_level", "") == "experienced":
            filtered.append(category)
    return filtered or category_list


def filter_project_domains_for_profile(project_domains, profile):
    domain = get_effective_domain(profile)
    if not domain:
        return deepcopy(project_domains)

    matched = []
    for item in project_domains:
        key = item["name"].strip().lower().replace("/", "_").replace(" ", "_")
        if key == domain:
            matched.append(deepcopy(item))
        elif domain == "web" and key in {"careertech", "edtech"}:
            matched.append(deepcopy(item))
        elif domain == "ai_ml" and key in {"data_science", "careertech"}:
            matched.append(deepcopy(item))
        elif domain == "cloud" and key == "web":
            matched.append(deepcopy(item))
    return matched or deepcopy(project_domains)


def get_profile_summary(profile):
    if not getattr(profile, "target_role", ""):
        return "Complete your student profile to see only the resources that match your goal."
    return PROFILE_SUMMARIES.get(
        profile.target_role,
        "Your dashboard is tailored to the role, domain, and experience level you selected.",
    )


def get_profile_change_request_summary(profile):
    if not (profile.pending_target_role or profile.pending_target_domain or profile.pending_experience_level):
        return ""
    parts = []
    if profile.pending_target_role:
        parts.append(f"Role: {dict(ROLE_CHOICES).get(profile.pending_target_role, profile.pending_target_role)}")
    if profile.pending_target_domain:
        parts.append(f"Domain: {dict(DOMAIN_CHOICES).get(profile.pending_target_domain, profile.pending_target_domain)}")
    if profile.pending_experience_level:
        parts.append(f"Experience: {dict(EXPERIENCE_CHOICES).get(profile.pending_experience_level, profile.pending_experience_level)}")
    return " | ".join(parts)


def get_profile_change_status_meta(profile):
    status = profile.role_change_status or ""
    status_map = {
        "pending": {
            "label": "Pending",
            "css": "pending",
            "message": "Your role update request is waiting for admin approval.",
        },
        "accepted": {
            "label": "Accepted",
            "css": "accepted",
            "message": "Your latest role update request was approved and is now active.",
        },
        "rejected": {
            "label": "Rejected",
            "css": "rejected",
            "message": "Your latest role update request was rejected. You can update and send a new request.",
        },
    }
    return status_map.get(status)


def build_dashboard_actions(profile):
    actions = [
        {
            "href": "/learn/",
            "icon": "book-open",
            "label": "Learn Path",
            "subtext": "Open only the tracks that match your selected role and domain.",
        },
        {
            "href": "/interview/",
            "icon": "target-lock",
            "label": "Interview Practice",
            "subtext": "Practice the interview categories that matter most for your target job.",
        },
        {
            "href": "/assessment/",
            "icon": "bulb",
            "label": "Project Ideas",
            "subtext": "See project ideas curated for your role, domain, and preparation level.",
        },
        {
            "href": "/resume/",
            "icon": "file",
            "label": "Resume Builder",
            "subtext": "Build a resume that supports your chosen career path.",
        },
    ]
    return actions


def filter_roadmap_catalog_for_profile(roadmap_catalog, profile):
    role = getattr(profile, "target_role", "")
    domain = get_effective_domain(profile)
    if not role and not domain:
        return deepcopy(roadmap_catalog)

    allowed_titles = {"Absolute Beginners", "Languages / Platforms"}
    if domain == "web":
        allowed_titles.update({"Web Development", "Frameworks", "Databases", "Design", "Best Practices"})
    elif domain == "ai_ml":
        allowed_titles.update({"AI & Machine Learning", "Data Analysis", "Computer Science", "Best Practices"})
    elif domain == "data_science":
        allowed_titles.update({"Data Analysis", "AI & Machine Learning", "Databases", "Computer Science"})
    elif domain == "cloud":
        allowed_titles.update({"DevOps", "Computer Science", "Databases", "Best Practices"})
    elif domain == "cybersecurity":
        allowed_titles.update({"Cyber Security", "Computer Science", "DevOps", "Best Practices"})
    elif domain == "android":
        allowed_titles.update({"Languages / Platforms", "Frameworks", "Computer Science"})
    elif domain in {"careertech", "edtech"}:
        allowed_titles.update({"Web Development", "Frameworks", "Databases", "AI & Machine Learning"})

    return [deepcopy(section) for section in roadmap_catalog if section["title"] in allowed_titles] or deepcopy(roadmap_catalog)


def filter_spotlight_paths_for_profile(spotlight_paths, profile):
    role = getattr(profile, "target_role", "")
    domain = get_effective_domain(profile)
    if role == "frontend":
        preferred = {"Frontend", "Placement Web Stack"}
    elif role == "backend":
        preferred = {"Backend Interview Prep", "Django Career Path"}
    elif role == "fullstack":
        preferred = {"Placement Web Stack", "Django Career Path", "Backend Interview Prep"}
    elif role == "data":
        preferred = {"AI Engineer Track", "DSA Practice Path"}
    elif role == "ai_ml":
        preferred = {"AI Engineer Track", "DSA Practice Path"}
    elif role == "devops":
        preferred = {"DevOps Foundation", "Backend Interview Prep"}
    elif role == "cybersecurity":
        preferred = {"DevOps Foundation", "DSA Practice Path"}
    elif role == "mobile":
        preferred = {"DSA Practice Path"}
    elif domain == "ai_ml":
        preferred = {"AI Engineer Track"}
    else:
        preferred = set()

    selected = [item for item in spotlight_paths if item["title"] in preferred]
    return selected or spotlight_paths[:3]
