from django.db.models import Count

from interview.models import Category, MockResult
from learn.models import Language, Topic


def _status_label(completed, in_progress):
    if completed:
        return "Completed"
    if in_progress:
        return "In progress"
    return "Pending"


def _status_color(status):
    if status == "Completed":
        return "green"
    if status == "In progress":
        return "amber"
    return "slate"


def _roadmap_item(title, slug, badge="Roadmap"):
    return {
        "title": title,
        "url": f"https://roadmap.sh/{slug}",
        "badge": badge,
    }


def build_user_roadmap(user, resume_built=False):
    results = MockResult.objects.filter(user=user).select_related("category")
    total_tests = results.count()
    avg_score = int(sum(r.percentage for r in results) / total_tests) if total_tests else 0
    strong_scores = results.filter(percentage__gte=70).count()

    skill_cards = []
    weak_skills = []
    for category in Category.objects.all():
        category_results = results.filter(category=category)
        attempts = category_results.count()
        avg = int(sum(r.percentage for r in category_results) / attempts) if attempts else 0
        if avg >= 70:
            level = "Strong"
        elif avg >= 40:
            level = "Improving"
        else:
            level = "Needs focus"
        skill_cards.append(
            {
                "name": category.name,
                "icon": category.icon,
                "avg": avg,
                "attempts": attempts,
                "level": level,
            }
        )
        if attempts == 0 or avg < 70:
            weak_skills.append(
                {
                    "name": category.name,
                    "avg": avg,
                    "attempts": attempts,
                }
            )

    weak_skills.sort(key=lambda item: (item["attempts"] > 0, item["avg"]))
    focus_skills = weak_skills[:3]

    phases = []

    phase_resume_done = resume_built
    phases.append(
        {
            "title": "Build your resume",
            "description": "Create a polished resume before starting company applications.",
            "status": _status_label(phase_resume_done, False),
            "color": _status_color(_status_label(phase_resume_done, False)),
            "meta": "Resume Builder",
        }
    )

    phase_assessment_done = total_tests >= 1
    phases.append(
        {
            "title": "Take baseline assessments",
            "description": "Measure your current level across aptitude and technical topics.",
            "status": _status_label(phase_assessment_done, total_tests > 0 and total_tests < 3),
            "color": _status_color(_status_label(phase_assessment_done, total_tests > 0 and total_tests < 3)),
            "meta": f"{total_tests} test{'s' if total_tests != 1 else ''}",
        }
    )

    phase_skills_done = strong_scores >= 2 or avg_score >= 70
    phase_skills_progress = total_tests >= 2
    phases.append(
        {
            "title": "Strengthen weak skills",
            "description": "Practice low-scoring topics until you consistently cross 70%.",
            "status": _status_label(phase_skills_done, phase_skills_progress and not phase_skills_done),
            "color": _status_color(_status_label(phase_skills_done, phase_skills_progress and not phase_skills_done)),
            "meta": f"Average score {avg_score}%",
        }
    )

    phase_interview_done = total_tests >= 5 and avg_score >= 60
    phase_interview_progress = total_tests >= 3
    phases.append(
        {
            "title": "Prepare for interviews",
            "description": "Use mock interviews regularly after building topic confidence.",
            "status": _status_label(phase_interview_done, phase_interview_progress and not phase_interview_done),
            "color": _status_color(_status_label(phase_interview_done, phase_interview_progress and not phase_interview_done)),
            "meta": "Mock Interview practice",
        }
    )

    phase_ready_done = resume_built and total_tests >= 5 and avg_score >= 70
    phase_ready_progress = resume_built or total_tests >= 3
    phases.append(
        {
            "title": "Apply with confidence",
            "description": "Track progress, refine your resume, and target placement drives.",
            "status": _status_label(phase_ready_done, phase_ready_progress and not phase_ready_done),
            "color": _status_color(_status_label(phase_ready_done, phase_ready_progress and not phase_ready_done)),
            "meta": "Placement-ready milestone",
        }
    )

    completed_count = sum(1 for phase in phases if phase["status"] == "Completed")
    overall_ready = round((completed_count / len(phases)) * 100)

    next_steps = []
    if not resume_built:
        next_steps.append("Build your resume to unlock your application-ready profile.")
    if total_tests < 3:
        next_steps.append("Take at least 3 assessments to identify reliable strengths and weak areas.")
    for skill in focus_skills:
        if skill["attempts"] == 0:
            next_steps.append(f"Start {skill['name']} assessment to get your first score.")
        elif skill["avg"] < 70:
            next_steps.append(f"Retake {skill['name']} and push the score above 70%.")
    if not next_steps:
        next_steps.append("Keep taking mock tests weekly to maintain momentum.")

    learning_tracks = []
    languages = Language.objects.annotate(
        topic_count=Count("topic", distinct=True),
        lesson_count=Count("topic__lesson", distinct=True),
    ).order_by("order", "name")

    for language in languages:
        topics = list(
            Topic.objects.filter(language=language)
            .annotate(lesson_count=Count("lesson", distinct=True))
            .order_by("order", "title")[:4]
        )
        learning_tracks.append(
            {
                "id": language.id,
                "name": language.name,
                "icon": language.icon,
                "description": language.description,
                "color": language.color,
                "topic_count": language.topic_count,
                "lesson_count": language.lesson_count,
                "topics": topics,
            }
        )

    featured_topics = list(
        Topic.objects.select_related("language")
        .annotate(lesson_count=Count("lesson", distinct=True))
        .order_by("language__order", "order", "title")[:8]
    )

    if featured_topics and total_tests < 2:
        next_steps.insert(
            0,
            f"Start with {featured_topics[0].language.name} -> {featured_topics[0].title} to build consistent topic practice.",
        )

    roadmap_catalog = [
        {
            "title": "Web Development",
            "description": "Build placement-ready web skills from beginner foundations to frontend, backend, and full stack delivery.",
            "items": [
                _roadmap_item("Frontend", "frontend", "Role"),
                _roadmap_item("Backend", "backend", "Role"),
                _roadmap_item("Full Stack", "full-stack", "Role"),
                _roadmap_item("QA", "qa", "Role"),
                _roadmap_item("API Design", "api-design", "Skill"),
                _roadmap_item("GraphQL", "graphql", "Skill"),
                _roadmap_item("Git and GitHub", "git-github", "Skill"),
                _roadmap_item("WordPress", "wordpress", "Platform"),
            ],
        },
        {
            "title": "Absolute Beginners",
            "description": "Start here if you want a simpler entry path before jumping into advanced frameworks or interview prep.",
            "items": [
                _roadmap_item("Frontend Beginner", "frontend?r=frontend-beginner", "Starter"),
                _roadmap_item("Backend Beginner", "backend?r=backend-beginner", "Starter"),
                _roadmap_item("DevOps Beginner", "devops?r=devops-beginner", "Starter"),
                _roadmap_item("Git and GitHub Beginner", "git-github?r=git-github-beginner", "Starter"),
            ],
        },
        {
            "title": "Frameworks",
            "description": "Pick a framework track once you know your target stack or your placement role focus.",
            "items": [
                _roadmap_item("React", "react", "Framework"),
                _roadmap_item("Vue", "vue", "Framework"),
                _roadmap_item("Angular", "angular", "Framework"),
                _roadmap_item("ASP.NET Core", "aspnet-core", "Framework"),
                _roadmap_item("Spring Boot", "spring-boot", "Framework"),
                _roadmap_item("Next.js", "nextjs", "Framework"),
                _roadmap_item("Laravel", "laravel", "Framework"),
                _roadmap_item("Django", "django", "Framework"),
                _roadmap_item("Ruby on Rails", "ruby-on-rails", "Framework"),
            ],
        },
        {
            "title": "Languages / Platforms",
            "description": "Sharpen your programming foundations and platform literacy for both interviews and project work.",
            "items": [
                _roadmap_item("SQL", "sql", "Language"),
                _roadmap_item("JavaScript", "javascript", "Language"),
                _roadmap_item("TypeScript", "typescript", "Language"),
                _roadmap_item("Node.js", "nodejs", "Platform"),
                _roadmap_item("Python", "python", "Language"),
                _roadmap_item("Java", "java", "Language"),
                _roadmap_item("C++", "cpp", "Language"),
                _roadmap_item("Rust", "rust", "Language"),
                _roadmap_item("Go", "golang", "Language"),
                _roadmap_item("PHP", "php", "Language"),
                _roadmap_item("Kotlin", "kotlin", "Language"),
                _roadmap_item("HTML", "html", "Core"),
                _roadmap_item("CSS", "css", "Core"),
                _roadmap_item("Swift & Swift UI", "swift", "Language"),
                _roadmap_item("Shell / Bash", "bash", "Tooling"),
                _roadmap_item("Ruby", "ruby", "Language"),
            ],
        },
        {
            "title": "DevOps",
            "description": "Learn deployment, infrastructure, cloud, and operations topics that modern backend teams expect.",
            "items": [
                _roadmap_item("DevOps", "devops", "Role"),
                _roadmap_item("DevSecOps", "devsecops", "Role"),
                _roadmap_item("Linux", "linux", "Platform"),
                _roadmap_item("Kubernetes", "kubernetes", "Platform"),
                _roadmap_item("Docker", "docker", "Platform"),
                _roadmap_item("AWS", "aws", "Cloud"),
                _roadmap_item("Terraform", "terraform", "Cloud"),
                _roadmap_item("Cloudflare", "cloudflare", "Cloud"),
            ],
        },
        {
            "title": "Databases",
            "description": "Use these tracks to strengthen storage, querying, caching, and search concepts.",
            "items": [
                _roadmap_item("PostgreSQL", "postgresql", "Database"),
                _roadmap_item("MongoDB", "mongodb", "Database"),
                _roadmap_item("Redis", "redis", "Database"),
                _roadmap_item("Elasticsearch", "elasticsearch", "Database"),
            ],
        },
        {
            "title": "Computer Science",
            "description": "These tracks support stronger system thinking for interviews, architecture rounds, and senior-level growth.",
            "items": [
                _roadmap_item("Computer Science", "computer-science", "Core"),
                _roadmap_item("System Design", "system-design", "Core"),
                _roadmap_item("Software Architect", "software-architect", "Role"),
                _roadmap_item("Design Architecture", "software-design-architecture", "Core"),
                _roadmap_item("Technical Writer", "technical-writer", "Career"),
                _roadmap_item("Data Structures & Algorithms", "datastructures-and-algorithms", "Interview"),
                _roadmap_item("Developer Relations", "devrel", "Career"),
                _roadmap_item("Code Review", "code-review", "Practice"),
            ],
        },
        {
            "title": "Design",
            "description": "Explore product-facing design skills that pair well with frontend and UX-oriented roles.",
            "items": [
                _roadmap_item("UX Design", "ux-design", "Design"),
                _roadmap_item("Design System", "design-system", "Design"),
            ],
        },
        {
            "title": "Best Practices",
            "description": "These are great for polishing real-world engineering habits after you know the basics.",
            "items": [
                _roadmap_item("AWS", "best-practices/aws", "Best Practice"),
                _roadmap_item("API Security", "best-practices/api-security", "Best Practice"),
                _roadmap_item("Backend Performance", "best-practices/backend-performance", "Best Practice"),
                _roadmap_item("Frontend Performance", "best-practices/frontend-performance", "Best Practice"),
                _roadmap_item("Code Review", "best-practices/code-review", "Best Practice"),
            ],
        },
        {
            "title": "AI & Machine Learning",
            "description": "Follow these tracks if you want to move into data, AI tools, models, and ML operations.",
            "items": [
                _roadmap_item("AI Engineer", "ai-engineer", "AI"),
                _roadmap_item("Data Engineer", "data-engineer", "Data"),
                _roadmap_item("Machine Learning", "machine-learning", "AI"),
                _roadmap_item("Prompt Engineering", "prompt-engineering", "AI"),
                _roadmap_item("MLOps", "mlops", "AI"),
                _roadmap_item("AI Red Teaming", "ai-red-teaming", "AI"),
                _roadmap_item("AI Agents", "ai-agents", "AI"),
                _roadmap_item("Claude Code", "claude-code", "AI"),
                _roadmap_item("Vibe Coding", "vibe-coding", "AI"),
            ],
        },
        {
            "title": "Data Analysis",
            "description": "Choose these tracks when you want a career path around analytics, BI, and data-driven decisions.",
            "items": [
                _roadmap_item("Data Analyst", "data-analyst", "Data"),
                _roadmap_item("AI and Data Scientist", "ai-data-scientist", "Data"),
                _roadmap_item("BI Analyst", "bi-analyst", "Data"),
            ],
        },
        {
            "title": "Management",
            "description": "These tracks help if your goals include leadership, architecture ownership, or communication-heavy roles.",
            "items": [
                _roadmap_item("Product Manager", "product-manager", "Career"),
                _roadmap_item("Engineering Manager", "engineering-manager", "Career"),
                _roadmap_item("Software Architect", "software-architect", "Career"),
                _roadmap_item("Technical Writer", "technical-writer", "Career"),
                _roadmap_item("Developer Relations", "devrel", "Career"),
            ],
        },
        {
            "title": "Game Development",
            "description": "Use these if you want to branch into gameplay systems, engines, or server-side game work.",
            "items": [
                _roadmap_item("Game Developer", "game-developer", "Career"),
                _roadmap_item("Server Side Game Developer", "server-side-game-developer", "Career"),
            ],
        },
        {
            "title": "Cyber Security",
            "description": "Security-focused paths for learners who want stronger defense, infrastructure, and secure engineering practices.",
            "items": [
                _roadmap_item("Cyber Security", "cyber-security", "Security"),
                _roadmap_item("AI Red Teaming", "ai-red-teaming", "Security"),
            ],
        },
        {
            "title": "Blockchain",
            "description": "Explore decentralized systems if you want to learn blockchain concepts and ecosystem tooling.",
            "items": [
                _roadmap_item("Blockchain", "blockchain", "Platform"),
            ],
        },
    ]

    spotlight_paths = [
        _roadmap_item("Placement Web Stack", "full-stack", "Recommended"),
        _roadmap_item("Django Career Path", "django", "Recommended"),
        _roadmap_item("Backend Interview Prep", "backend", "Recommended"),
        _roadmap_item("DSA Practice Path", "datastructures-and-algorithms", "Recommended"),
        _roadmap_item("DevOps Foundation", "devops", "Recommended"),
        _roadmap_item("AI Engineer Track", "ai-engineer", "Recommended"),
    ]

    return {
        "overall_ready": overall_ready,
        "total_tests": total_tests,
        "avg_score": avg_score,
        "resume_built": resume_built,
        "phases": phases,
        "skill_cards": skill_cards,
        "focus_skills": focus_skills,
        "next_steps": next_steps[:4],
        "recent_results": results.order_by("-taken_at")[:5],
        "learning_tracks": learning_tracks,
        "featured_topics": featured_topics,
        "roadmap_catalog": roadmap_catalog,
        "spotlight_paths": spotlight_paths,
    }
