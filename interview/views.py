import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Question, MockResult


def _display_icon(icon_value, name):
    icon = (icon_value or '').strip()
    if not icon or icon == '??':
        return (name or 'NA')[:2]
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
    if request.method == 'POST':
        selected = request.POST.get('answer', '')
        answers = request.session.get('quiz_answers', {})
        answers[str(question_no)] = selected
        request.session['quiz_answers'] = answers
        request.session.modified = True
        if question_no < total:
            return redirect('quiz_question', question_no=question_no+1)
        else:
            return redirect('quiz_result')
    question = get_object_or_404(Question, id=question_ids[question_no-1])
    answers = request.session.get('quiz_answers', {})
    saved_answer = answers.get(str(question_no), '')
    return render(request, 'interview/quiz.html', {
        'question': question,
        'question_no': question_no,
        'total': total,
        'progress': int((question_no / total) * 100),
        'saved_answer': saved_answer,
        'category_id': category_id,
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
