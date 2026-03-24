import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.safestring import mark_safe

from accounts.models import UserProfile
from accounts.personalization import filter_categories_for_profile, get_profile_summary

from .models import Category, MockResult, Question


def _display_icon(category_or_icon, name=None):
    if hasattr(category_or_icon, "name"):
        category = category_or_icon
        name = category.name
        icon = (category.icon or "").strip()
        if category.logo_image:
            try:
                return mark_safe(
                    f'<img src="{category.logo_image.url}" alt="{name}" style="width:42px;height:42px;object-fit:contain;display:block;" />'
                )
            except ValueError:
                pass
        if category.logo_url:
            return mark_safe(
                f'<img src="{category.logo_url}" alt="{name}" style="width:42px;height:42px;object-fit:contain;display:block;" onerror="this.outerHTML=\'<span class=&quot;cat-fallback&quot;>{(name or "NA")[:2]}</span>\'" />'
            )
    else:
        icon = (category_or_icon or "").strip()

    key = (name or "").strip().lower()
    icon_map = {
        "python": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#3776AB" d="M11.963 2c-2.092 0-4.086.188-5.33.627C4.797 3.275 4.5 4.194 4.5 5.68v2.133h7v.711H1.875C.835 8.524 0 9.354 0 10.39v3.221c0 1.036.9 1.964 1.875 2.25 1.237.363 2.513.535 4.788.535 2.138 0 4.087-.188 5.3-.627 1.477-.533 1.537-1.658 1.537-3.053v-2.134h-7V9.87h10.5c1.04 0 1.5-.91 1.5-1.866V4.79c0-.915-.773-1.603-1.5-1.824C15.628 2.327 14.055 2 11.963 2Zm-3.879 1.706c.497 0 .916.412.916.92 0 .505-.42.916-.916.916a.915.915 0 0 1-.918-.917c0-.507.421-.919.918-.919Z"/><path fill="#FFD43B" d="M12.037 22c2.092 0 4.086-.188 5.33-.627 1.836-.648 2.133-1.567 2.133-3.053v-2.133h-7v-.711H22.125c1.04 0 1.875-.83 1.875-1.866V10.39c0-1.036-.9-1.964-1.875-2.25-1.237-.363-2.513-.535-4.788-.535-2.138 0-4.087.188-5.3.627-1.477.533-1.537 1.658-1.537 3.053v2.134h7v.711H7c-1.04 0-1.5.91-1.5 1.866v3.214c0 .915.773 1.603 1.5 1.824 1.372.639 2.945.966 5.037.966Zm3.879-1.706c-.497 0-.916-.412-.916-.92 0-.505.42-.916.916-.916.506 0 .918.411.918.917a.916.916 0 0 1-.918.919Z"/></svg>',
        "dsa": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7 4h10l3 5-3 5H7L4 9l3-5Zm.8 2L6.4 9l1.4 3h8.4l1.4-3-1.4-3H7.8ZM5 16h14v2H5v-2Zm3 4h8v2H8v-2Z"/></svg>',
        "web dev": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#E34F26" d="M4.136 3h15.728l-1.43 16.09L12 21l-6.434-1.91L4.136 3Zm12.782 5.218.179-2.006H6.903l.537 6.03h6.913l-.247 2.754-2.106.572-2.106-.572-.135-1.514H7.88l.265 2.967L12 17.58l3.855-1.13.53-5.946H9.207l-.18-2.286h7.891Z"/></svg>',
        "django": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#0C4B33" d="M9.996 4.5h3.074v10.41c-1.324.252-2.3.353-3.368.353-3.177 0-4.838-1.43-4.838-4.17 0-2.638 1.755-4.347 4.473-4.347.421 0 .742.033 1.165.126V4.5Zm0 4.841a2.66 2.66 0 0 0-.91-.151c-1.36 0-2.147.833-2.147 2.299 0 1.43.757 2.21 2.122 2.21.295 0 .537-.025.935-.086V9.34Zm7.886-2.4v7.146c0 2.463-.185 3.642-.74 4.665-.513.983-1.19 1.607-2.584 2.267l-2.853-1.348c1.394-.648 2.071-1.23 2.494-2.105.444-.897.586-1.936.586-4.711V6.941h3.097Zm-3.097-4.43h3.097V5.69h-3.097V2.511Z"/></svg>',
        "dbms": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 3c-4.97 0-9 1.343-9 3v12c0 1.657 4.03 3 9 3s9-1.343 9-3V6c0-1.657-4.03-3-9-3Zm0 2c4.418 0 7 .99 7 1s-2.582 1-7 1-7-.99-7-1 2.582-1 7-1Zm0 5c4.418 0 7-.99 7-1v3c0 .01-.077.128-.43.29-.407.187-.998.368-1.73.517C15.39 13.11 13.754 13.3 12 13.3c-1.754 0-3.39-.19-4.84-.493-.732-.149-1.323-.33-1.73-.517C5.077 12.128 5 12.01 5 12V9c0 .01 2.582 1 7 1Zm0 8.3c-1.754 0-3.39-.19-4.84-.493-.732-.149-1.323-.33-1.73-.517C5.077 17.128 5 17.01 5 17v-3c1.56.86 4.36 1.3 7 1.3s5.44-.44 7-1.3v3c0 .01-.077.128-.43.29-.407.187-.998.368-1.73.517-1.45.304-3.086.493-4.84.493Z"/></svg>',
        "computer networks": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M9 3a2 2 0 0 1 2 2v1h2V5a2 2 0 1 1 4 0v3a2 2 0 0 1-2 2h-2v2h2a2 2 0 0 1 2 2v1h1a2 2 0 1 1 0 2h-3v-3a2 2 0 0 1 2-2h-2V10h-2v2H9a2 2 0 0 1 2 2v3H8a2 2 0 1 1 0-2h1v-1a2 2 0 0 1 2-2h2v-2H9a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Zm0 2v3h6V5H9Z"/></svg>',
        "operating systems": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8A2.5 2.5 0 0 1 17.5 16H13v2h3a1 1 0 1 1 0 2H8a1 1 0 1 1 0-2h3v-2H6.5A2.5 2.5 0 0 1 4 13.5v-8Zm2.5-.5a.5.5 0 0 0-.5.5v8c0 .276.224.5.5.5h11a.5.5 0 0 0 .5-.5v-8a.5.5 0 0 0-.5-.5h-11Z"/></svg>',
        "oops": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7 4a3 3 0 0 1 3 3v1h4V7a3 3 0 1 1 6 0v6a3 3 0 0 1-3 3h-1v2h1a1 1 0 1 1 0 2H7a3 3 0 0 1-3-3v-1a3 3 0 0 1 3-3h7v-3H7a3 3 0 0 1 0-6Zm10 2a1 1 0 0 0-1 1v1h2V7a1 1 0 0 0-1-1ZM7 15a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h7v-3H7ZM7 6a1 1 0 1 0 0 2h1V7a1 1 0 0 0-1-1Z"/></svg>',
        "system design": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M3 5.75A2.75 2.75 0 0 1 5.75 3h4.5A2.75 2.75 0 0 1 13 5.75v1.5A2.75 2.75 0 0 1 10.25 10h-1v1h5.5v-1h-1A2.75 2.75 0 0 1 11 7.25v-1.5A2.75 2.75 0 0 1 13.75 3h4.5A2.75 2.75 0 0 1 21 5.75v1.5A2.75 2.75 0 0 1 18.25 10h-1v4h1A2.75 2.75 0 0 1 21 16.75v1.5A2.75 2.75 0 0 1 18.25 21h-4.5A2.75 2.75 0 0 1 11 18.25v-1.5A2.75 2.75 0 0 1 13.75 14h1v-1H9.25v1h1A2.75 2.75 0 0 1 13 16.75v1.5A2.75 2.75 0 0 1 10.25 21h-4.5A2.75 2.75 0 0 1 3 18.25v-1.5A2.75 2.75 0 0 1 5.75 14h1v-4h-1A2.75 2.75 0 0 1 3 7.25v-1.5Zm2 0v1.5c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-1.5a.75.75 0 0 0-.75-.75h-4.5a.75.75 0 0 0-.75.75Zm8 0v1.5c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-1.5a.75.75 0 0 0-.75-.75h-4.5a.75.75 0 0 0-.75.75Zm0 11v1.5c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-1.5a.75.75 0 0 0-.75-.75h-4.5a.75.75 0 0 0-.75.75Zm-8 0v1.5c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-1.5a.75.75 0 0 0-.75-.75h-4.5a.75.75 0 0 0-.75.75Z"/></svg>',
        "hr questions": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16 11a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm-8 2a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm8 2c-3.33 0-8 1.67-8 5v1h16v-1c0-3.33-4.67-5-8-5Zm-8 0c-.29 0-.62.02-.97.05C4.41 15.27 0 16.56 0 20v1h6v-1c0-1.94.81-3.61 2.23-4.85A8.62 8.62 0 0 0 8 15Z"/></svg>',
        "aptitude": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M9.5 2A7.5 7.5 0 0 0 7 16.57V20a2 2 0 0 0 2 2h1v-5H8.5a1 1 0 0 1 0-2H10v-2H8.5a1 1 0 0 1 0-2H10V9H8.5a1 1 0 0 1 0-2H10V4.06A7.3 7.3 0 0 0 9.5 2ZM14 4.27V7h1.5a1 1 0 1 1 0 2H14v2h1.5a1 1 0 1 1 0 2H14v2h1.5a1 1 0 1 1 0 2H14v5h1a2 2 0 0 0 2-2v-3.43A7.5 7.5 0 0 0 14 4.27ZM12 2a9.5 9.5 0 0 1 6.08 16.8A1 1 0 0 0 18 19.56V20a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4v-.44a1 1 0 0 0-.08-.76A9.5 9.5 0 0 1 12 2Z"/></svg>',
    }
    if key in icon_map:
        return mark_safe(icon_map[key])
    if not icon or icon == "??" or icon.startswith("ð") or icon.startswith("â") or icon.startswith("Ã"):
        return mark_safe(f'<span class="cat-fallback">{(name or "NA")[:2]}</span>')
    return mark_safe(icon)


@login_required
def interview_home(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    categories = filter_categories_for_profile(Category.objects.all(), profile)
    recent_results = MockResult.objects.filter(user=request.user)[:5]
    total_tests = MockResult.objects.filter(user=request.user).count()
    for category in categories:
        category.display_icon = _display_icon(category)
    for result in recent_results:
        result.category.display_icon = _display_icon(result.category)
    return render(
        request,
        "interview/interview.html",
        {
            "categories": categories,
            "recent_results": recent_results,
            "total_tests": total_tests,
            "profile_summary": get_profile_summary(profile),
            "target_role_label": profile.get_target_role_display() if profile.target_role else "Student",
        },
    )


@login_required
def start_test(request, category_id):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    allowed_ids = {category.id for category in filter_categories_for_profile(Category.objects.all(), profile)}
    if category_id not in allowed_ids:
        return redirect("interview_home")
    category = get_object_or_404(Category, id=category_id)
    questions = list(Question.objects.filter(category=category))
    if len(questions) < 5:
        return redirect("interview_home")
    selected = random.sample(questions, min(20, len(questions)))
    request.session["quiz_questions"] = [q.id for q in selected]
    request.session["quiz_category"] = category_id
    request.session["quiz_answers"] = {}
    return redirect("quiz_question", question_no=1)


@login_required
def quiz_question(request, question_no):
    question_ids = request.session.get("quiz_questions", [])
    category_id = request.session.get("quiz_category")
    if not question_ids:
        return redirect("interview_home")
    total = len(question_ids)
    if question_no < 1 or question_no > total:
        return redirect("quiz_result")
    question = get_object_or_404(Question, id=question_ids[question_no - 1])
    answers = request.session.get("quiz_answers", {})
    saved_answer = answers.get(str(question_no), "")

    if request.method == "POST":
        action = request.POST.get("action", "answer")
        if action == "continue":
            if question_no < total:
                return redirect("quiz_question", question_no=question_no + 1)
            return redirect("quiz_result")

        selected = request.POST.get("answer", "")
        answers[str(question_no)] = selected
        request.session["quiz_answers"] = answers
        request.session.modified = True
        saved_answer = selected

        if selected:
            is_correct = selected.upper() == question.correct_option.upper()
            feedback_context = {
                "question": question,
                "question_no": question_no,
                "total": total,
                "progress": int((question_no / total) * 100),
                "saved_answer": saved_answer,
                "category_id": category_id,
                "show_feedback": True,
                "is_correct": is_correct,
                "correct_option": question.correct_option,
            }
            return render(request, "interview/quiz.html", feedback_context)

        if question_no < total:
            return redirect("quiz_question", question_no=question_no + 1)
        return redirect("quiz_result")

    return render(
        request,
        "interview/quiz.html",
        {
            "question": question,
            "question_no": question_no,
            "total": total,
            "progress": int((question_no / total) * 100),
            "saved_answer": saved_answer,
            "category_id": category_id,
            "show_feedback": False,
        },
    )


@login_required
def exit_quiz(request):
    for key in ["quiz_questions", "quiz_category", "quiz_answers"]:
        request.session.pop(key, None)
    return redirect("interview_home")


@login_required
def quiz_result(request):
    question_ids = request.session.get("quiz_questions", [])
    category_id = request.session.get("quiz_category")
    answers = request.session.get("quiz_answers", {})
    if not question_ids or not category_id:
        return redirect("interview_home")

    questions = Question.objects.filter(id__in=question_ids)
    q_map = {q.id: q for q in questions}
    results = []
    score = 0

    for i, qid in enumerate(question_ids, 1):
        q = q_map.get(qid)
        if not q:
            continue
        user_ans = answers.get(str(i), "")
        is_correct = user_ans.upper() == q.correct_option.upper() if user_ans else False
        if is_correct:
            score += 1
        results.append(
            {
                "question": q,
                "user_answer": user_ans,
                "is_correct": is_correct,
                "correct_option": q.correct_option,
            }
        )

    total = len(question_ids)
    wrong_count = total - score
    percentage = int((score / total) * 100) if total else 0
    category = get_object_or_404(Category, id=category_id)
    category.display_icon = _display_icon(category)

    MockResult.objects.create(
        user=request.user,
        category=category,
        score=score,
        total=total,
        percentage=percentage,
    )

    for key in ["quiz_questions", "quiz_category", "quiz_answers"]:
        request.session.pop(key, None)

    if percentage >= 80:
        grade = "Excellent"
        grade_color = "green"
    elif percentage >= 60:
        grade = "Good"
        grade_color = "blue"
    elif percentage >= 40:
        grade = "Average"
        grade_color = "amber"
    else:
        grade = "Needs Work"
        grade_color = "red"

    return render(
        request,
        "interview/result.html",
        {
            "score": score,
            "total": total,
            "wrong_count": wrong_count,
            "percentage": percentage,
            "grade": grade,
            "grade_color": grade_color,
            "results": results,
            "category": category,
        },
    )
