from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from interview.models import MockResult, Category
from .roadmap import build_user_roadmap


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Real data
    results = MockResult.objects.filter(user=request.user)
    total_tests = results.count()
    avg_score = 0
    if total_tests > 0:
        avg_score = int(sum(r.percentage for r in results) / total_tests)

    # Skill progress per category
    skill_progress = []
    for cat in Category.objects.all():
        cat_results = results.filter(category=cat)
        if cat_results.exists():
            avg = int(sum(r.percentage for r in cat_results) / cat_results.count())
        else:
            avg = 0
        skill_progress.append({
            'name': cat.name,
            'icon': cat.icon,
            'avg': avg,
        })

    # Recent activity
    recent = results.order_by('-taken_at')[:5]

    # Resume built check — simple session flag
    resume_built = request.session.get('resume_built', False)

    context = {
        'total_tests': total_tests,
        'avg_score': avg_score,
        'skill_progress': skill_progress,
        'recent': recent,
        'resume_built': resume_built,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    from django.contrib.auth.models import User
    total_users = User.objects.filter(is_superuser=False).count()
    recent_users = User.objects.filter(is_superuser=False).order_by('-date_joined')[:10]
    total_tests = MockResult.objects.count()
    context = {
        'total_users': total_users,
        'recent_users': recent_users,
        'total_tests': total_tests,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def roadmap(request):
    resume_built = request.session.get('resume_built', False)
    context = build_user_roadmap(request.user, resume_built=resume_built)
    return render(request, 'dashboard/roadmap.html', context)
