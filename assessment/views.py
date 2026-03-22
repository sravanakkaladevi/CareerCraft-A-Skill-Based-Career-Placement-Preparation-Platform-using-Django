import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SkillTopic, SkillQuestion, SkillScore


@login_required
def assessment_home(request):
    topics = SkillTopic.objects.all()
    latest_scores = SkillScore.get_latest_per_topic(request.user)
    return render(request, 'assessment/assessment.html', {
        'topics': topics,
        'latest_scores': latest_scores,
    })


@login_required
def start_assessment(request, topic_id):
    topic = get_object_or_404(SkillTopic, id=topic_id)
    questions = list(SkillQuestion.objects.filter(topic=topic))
    if len(questions) < 5:
        return redirect('assessment_home')
    selected = random.sample(questions, min(10, len(questions)))
    request.session['assess_questions'] = [q.id for q in selected]
    request.session['assess_topic'] = topic_id
    request.session['assess_answers'] = {}
    return redirect('assess_question', question_no=1)


@login_required
def assess_question(request, question_no):
    question_ids = request.session.get('assess_questions', [])
    topic_id = request.session.get('assess_topic')
    if not question_ids:
        return redirect('assessment_home')
    total = len(question_ids)
    if question_no < 1 or question_no > total:
        return redirect('assess_result')
    if request.method == 'POST':
        selected = request.POST.get('answer', '')
        answers = request.session.get('assess_answers', {})
        answers[str(question_no)] = selected
        request.session['assess_answers'] = answers
        request.session.modified = True
        if question_no < total:
            return redirect('assess_question', question_no=question_no+1)
        else:
            return redirect('assess_result')
    question = get_object_or_404(SkillQuestion, id=question_ids[question_no-1])
    saved_answer = request.session.get('assess_answers', {}).get(str(question_no), '')
    return render(request, 'assessment/assess_quiz.html', {
        'question': question,
        'question_no': question_no,
        'total': total,
        'progress': int((question_no / total) * 100),
        'saved_answer': saved_answer,
        'question_range': list(range(1, total + 1)),
    })


@login_required
def assess_result(request):
    question_ids = request.session.get('assess_questions', [])
    topic_id = request.session.get('assess_topic')
    answers = request.session.get('assess_answers', {})
    if not question_ids or not topic_id:
        return redirect('assessment_home')
    questions = SkillQuestion.objects.filter(id__in=question_ids)
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
    percentage = int((score / total) * 100) if total else 0
    topic = get_object_or_404(SkillTopic, id=topic_id)
    SkillScore.objects.create(
        user=request.user,
        topic=topic,
        score=score,
        total=total,
        percentage=percentage,
    )
    for key in ['assess_questions', 'assess_topic', 'assess_answers']:
        request.session.pop(key, None)
    if percentage >= 80:
        grade, grade_color = 'Excellent', 'green'
        suggestion = 'Outstanding! You have strong knowledge in this area.'
    elif percentage >= 60:
        grade, grade_color = 'Good', 'blue'
        suggestion = 'Good understanding. Review weak areas to improve further.'
    elif percentage >= 40:
        grade, grade_color = 'Average', 'amber'
        suggestion = 'Needs improvement. Focus on the topics you got wrong.'
    else:
        grade, grade_color = 'Needs Work', 'red'
        suggestion = 'Significant gaps found. Revise fundamentals before retaking.'
    return render(request, 'assessment/assess_result.html', {
        'score': score,
        'total': total,
        'percentage': percentage,
        'grade': grade,
        'grade_color': grade_color,
        'suggestion': suggestion,
        'results': results,
        'topic': topic,
        'wrong_count': total - score,
    })