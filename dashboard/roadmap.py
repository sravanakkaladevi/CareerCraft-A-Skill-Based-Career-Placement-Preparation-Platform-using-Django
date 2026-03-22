from interview.models import Category, MockResult


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
    }
