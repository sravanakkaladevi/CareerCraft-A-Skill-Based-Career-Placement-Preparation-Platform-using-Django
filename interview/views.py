import random
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Question, MockResult


def _display_icon(icon_value, name):
    icon = (icon_value or '').strip()
    key = (name or '').strip().lower()
    icon_map = {
        'python': '<i class="devicon-python-plain colored"></i>',
        'dsa': '<i class="devicon-cplusplus-plain colored"></i>',
        'web dev': '<i class="devicon-html5-plain colored"></i>',
        'django': '<i class="devicon-django-plain colored"></i>',
        'dbms': '<i class="devicon-mysql-plain colored"></i>',
        'computer networks': '<i class="devicon-nodejs-plain colored"></i>',
        'operating systems': '<i class="devicon-linux-plain"></i>',
        'oops': '<i class="devicon-java-plain colored"></i>',
        'system design': '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M3 5.75A2.75 2.75 0 0 1 5.75 3h4.5A2.75 2.75 0 0 1 13 5.75v1.5A2.75 2.75 0 0 1 10.25 10h-1v1h5.5v-1h-1A2.75 2.75 0 0 1 11 7.25v-1.5A2.75 2.75 0 0 1 13.75 3h4.5A2.75 2.75 0 0 1 21 5.75v1.5A2.75 2.75 0 0 1 18.25 10h-1v4h1A2.75 2.75 0 0 1 21 16.75v1.5A2.75 2.75 0 0 1 18.25 21h-4.5A2.75 2.75 0 0 1 11 18.25v-1.5A2.75 2.75 0 0 1 13.75 14h1v-1H9.25v1h1A2.75 2.75 0 0 1 13 16.75v1.5A2.75 2.75 0 0 1 10.25 21h-4.5A2.75 2.75 0 0 1 3 18.25v-1.5A2.75 2.75 0 0 1 5.75 14h1v-4h-1A2.75 2.75 0 0 1 3 7.25v-1.5Zm2 0v1.5c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-1.5a.75.75 0 0 0-.75-.75h-4.5a.75.75 0 0 0-.75.75Zm8 0v1.5c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-1.5a.75.75 0 0 0-.75-.75h-4.5a.75.75 0 0 0-.75.75Zm0 11v1.5c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-1.5a.75.75 0 0 0-.75-.75h-4.5a.75.75 0 0 0-.75.75Zm-8 0v1.5c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-1.5a.75.75 0 0 0-.75-.75h-4.5a.75.75 0 0 0-.75.75Z"/></svg>',
        'hr questions': '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16 11a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm-8 2a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm8 2c-3.33 0-8 1.67-8 5v1h16v-1c0-3.33-4.67-5-8-5Zm-8 0c-.29 0-.62.02-.97.05C4.41 15.27 0 16.56 0 20v1h6v-1c0-1.94.81-3.61 2.23-4.85A8.62 8.62 0 0 0 8 15Z"/></svg>',
        'aptitude': '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M9.5 2A7.5 7.5 0 0 0 7 16.57V20a2 2 0 0 0 2 2h1v-5H8.5a1 1 0 0 1 0-2H10v-2H8.5a1 1 0 0 1 0-2H10V9H8.5a1 1 0 0 1 0-2H10V4.06A7.3 7.3 0 0 0 9.5 2ZM14 4.27V7h1.5a1 1 0 1 1 0 2H14v2h1.5a1 1 0 1 1 0 2H14v2h1.5a1 1 0 1 1 0 2H14v5h1a2 2 0 0 0 2-2v-3.43A7.5 7.5 0 0 0 14 4.27ZM12 2a9.5 9.5 0 0 1 6.08 16.8A1 1 0 0 0 18 19.56V20a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4v-.44a1 1 0 0 0-.08-.76A9.5 9.5 0 0 1 12 2Z"/></svg>',
    }
    if key in icon_map:
        return mark_safe(icon_map[key])
    if not icon or icon == '??':
        return mark_safe(f'<span class="cat-fallback">{(name or "NA")[:2]}</span>')
    return icon


@login_required
def interview_home(request):
    categories = Category.objects.all()
    recent_results = MockResult.objects.filter(user=request.user)[:5]
    for category in categories:
        category.display_icon = _display_icon(category.icon, category.name)
    for result in recent_results:
        result.category.display_icon = _display_icon(result.category.icon, result.category.name)
    return render(request, 'interview/interview.html', {
        'categories': categories,
        'recent_results': recent_results,
    })


@login_required
def start_test(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    questions = list(Question.objects.filter(category=category))
    if len(questions) < 5:
        return redirect('interview_home')
    selected = random.sample(questions, min(20, len(questions)))
    request.session['quiz_questions'] = [q.id for q in selected]
    request.session['quiz_category'] = category_id
    request.session['quiz_answers'] = {}
    return redirect('quiz_question', question_no=1)


@login_required
def quiz_question(request, question_no):
    question_ids = request.session.get('quiz_questions', [])
    category_id = request.session.get('quiz_category')
    if not question_ids:
        return redirect('interview_home')
    total = len(question_ids)
    if question_no < 1 or question_no > total:
        return redirect('quiz_result')
    question = get_object_or_404(Question, id=question_ids[question_no-1])
    answers = request.session.get('quiz_answers', {})
    saved_answer = answers.get(str(question_no), '')

    if request.method == 'POST':
        action = request.POST.get('action', 'answer')
        if action == 'continue':
            if question_no < total:
                return redirect('quiz_question', question_no=question_no+1)
            return redirect('quiz_result')

        selected = request.POST.get('answer', '')
        answers[str(question_no)] = selected
        request.session['quiz_answers'] = answers
        request.session.modified = True
        saved_answer = selected

        if selected:
            is_correct = selected.upper() == question.correct_option.upper()
            feedback_context = {
                'question': question,
                'question_no': question_no,
                'total': total,
                'progress': int((question_no / total) * 100),
                'saved_answer': saved_answer,
                'category_id': category_id,
                'show_feedback': True,
                'is_correct': is_correct,
                'correct_option': question.correct_option,
            }
            return render(request, 'interview/quiz.html', feedback_context)

        if question_no < total:
            return redirect('quiz_question', question_no=question_no+1)
        return redirect('quiz_result')

    return render(request, 'interview/quiz.html', {
        'question': question,
        'question_no': question_no,
        'total': total,
        'progress': int((question_no / total) * 100),
        'saved_answer': saved_answer,
        'category_id': category_id,
        'show_feedback': False,
    })


@login_required
def exit_quiz(request):
    for key in ['quiz_questions', 'quiz_category', 'quiz_answers']:
        request.session.pop(key, None)
    return redirect('interview_home')


@login_required
def quiz_result(request):
    question_ids = request.session.get('quiz_questions', [])
    category_id = request.session.get('quiz_category')
    answers = request.session.get('quiz_answers', {})
    if not question_ids or not category_id:
        return redirect('interview_home')

    questions = Question.objects.filter(id__in=question_ids)
    q_map = {q.id: q for q in questions}
    results = []
    score = 0

    for i, qid in enumerate(question_ids, 1):
        q = q_map.get(qid)
        if not q:
            continue
        user_ans = answers.get(str(i), '')
        is_correct = user_ans.upper() == q.correct_option.upper() if user_ans else False
        if is_correct:
            score += 1
        results.append({
            'question': q,
            'user_answer': user_ans,
            'is_correct': is_correct,
            'correct_option': q.correct_option,
        })

    total = len(question_ids)
    wrong_count = total - score
    percentage = int((score / total) * 100) if total else 0
    category = get_object_or_404(Category, id=category_id)
    category.display_icon = _display_icon(category.icon, category.name)

    MockResult.objects.create(
        user=request.user,
        category=category,
        score=score,
        total=total,
        percentage=percentage,
    )

    # Clear session AFTER saving result
    for key in ['quiz_questions', 'quiz_category', 'quiz_answers']:
        request.session.pop(key, None)

    if percentage >= 80:
        grade = 'Excellent'
        grade_color = 'green'
    elif percentage >= 60:
        grade = 'Good'
        grade_color = 'blue'
    elif percentage >= 40:
        grade = 'Average'
        grade_color = 'amber'
    else:
        grade = 'Needs Work'
        grade_color = 'red'

    return render(request, 'interview/result.html', {
        'score': score,
        'total': total,
        'wrong_count': wrong_count,
        'percentage': percentage,
        'grade': grade,
        'grade_color': grade_color,
        'results': results,
        'category': category,
    })
