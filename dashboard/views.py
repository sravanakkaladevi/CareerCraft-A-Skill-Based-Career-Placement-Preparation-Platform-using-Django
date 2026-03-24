from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from interview.models import MockResult, Category
from interview.models import Question
from assessment.models import SkillScore, SkillTopic
from assessment.models import SkillQuestion
from learn.models import BlogComment, BlogPost
from accounts.models import UserProfile
from accounts.personalization import (
    approve_pending_profile_change,
    build_dashboard_actions,
    clear_pending_profile_change,
    filter_categories_for_profile,
    get_profile_change_request_summary,
    get_profile_summary,
)
from .models import SiteBranding
from .roadmap import build_user_roadmap
from .forms import (
    AssessmentQuestionForm,
    AssessmentTopicForm,
    BlogPostForm,
    InterviewCategoryForm,
    InterviewQuestionForm,
    SiteBrandingForm,
)


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # Real data
    results = MockResult.objects.filter(user=request.user)
    total_tests = results.count()
    avg_score = 0
    if total_tests > 0:
        avg_score = int(sum(r.percentage for r in results) / total_tests)

    # Skill progress per category
    skill_progress = []
    recommended_categories = filter_categories_for_profile(Category.objects.all(), profile)
    for cat in recommended_categories:
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
        'profile_summary': get_profile_summary(profile),
        'profile_complete': profile.is_profile_complete,
        'quick_actions': build_dashboard_actions(profile),
        'target_role_label': profile.get_target_role_display() if profile.target_role else 'Student',
        'target_domain_label': profile.get_target_domain_display() if profile.target_domain else 'General preparation',
        'experience_level_label': profile.get_experience_level_display(),
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    if request.method == 'POST':
        action = request.POST.get('action')
        profile_id = request.POST.get('profile_id')
        pending_profile = UserProfile.objects.filter(id=profile_id).first()
        if pending_profile and pending_profile.has_pending_role_change:
            if action == 'approve_profile_change':
                approve_pending_profile_change(pending_profile)
                pending_profile.save()
                from django.contrib import messages
                messages.success(request, f'Approved role update for {pending_profile.user.username}.')
            elif action == 'reject_profile_change':
                clear_pending_profile_change(pending_profile)
                pending_profile.save()
                from django.contrib import messages
                messages.info(request, f'Rejected pending role update for {pending_profile.user.username}.')
        return redirect('admin_dashboard')
    from django.contrib.auth.models import User
    total_users = User.objects.filter(is_superuser=False).count()
    recent_users = User.objects.filter(is_superuser=False).order_by('-date_joined')[:10]
    total_tests = MockResult.objects.count()
    total_assessments = SkillScore.objects.count()
    total_categories = Category.objects.count()
    total_questions = sum(category.question_count() for category in Category.objects.all())
    total_topics = SkillTopic.objects.count()
    total_blog_posts = BlogPost.objects.count()
    branding = SiteBranding.get_solo()
    pending_profile_requests = []
    for profile in UserProfile.objects.filter(user__is_superuser=False).select_related('user').order_by('-role_change_requested_at'):
        if profile.has_pending_role_change:
            pending_profile_requests.append(
                {
                    'profile': profile,
                    'summary': get_profile_change_request_summary(profile),
                }
            )
    context = {
        'total_users': total_users,
        'recent_users': recent_users,
        'total_tests': total_tests,
        'total_assessments': total_assessments,
        'total_categories': total_categories,
        'total_questions': total_questions,
        'total_topics': total_topics,
        'total_blog_posts': total_blog_posts,
        'branding': branding,
        'pending_profile_requests': pending_profile_requests,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def content_manager(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    branding = SiteBranding.get_solo()
    branding_form = SiteBrandingForm(instance=branding, prefix='branding')
    interview_category_form = InterviewCategoryForm(prefix='interview_category')
    interview_question_form = InterviewQuestionForm(prefix='interview_question')
    assessment_topic_form = AssessmentTopicForm(prefix='assessment_topic')
    assessment_question_form = AssessmentQuestionForm(prefix='assessment_question')
    blog_post_form = BlogPostForm(prefix='blog_post')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'save_branding':
            branding_form = SiteBrandingForm(request.POST, request.FILES, instance=branding, prefix='branding')
            if branding_form.is_valid():
                branding_form.save()
                messages.success(request, 'Site branding updated.')
                return redirect('content_manager')

        elif action == 'add_interview_category':
            interview_category_form = InterviewCategoryForm(request.POST, request.FILES, prefix='interview_category')
            if interview_category_form.is_valid():
                interview_category_form.save()
                messages.success(request, 'Interview category created.')
                return redirect('content_manager')

        elif action == 'add_interview_question':
            interview_question_form = InterviewQuestionForm(request.POST, prefix='interview_question')
            if interview_question_form.is_valid():
                interview_question_form.save()
                messages.success(request, 'Interview question created.')
                return redirect('content_manager')

        elif action == 'add_assessment_topic':
            assessment_topic_form = AssessmentTopicForm(request.POST, request.FILES, prefix='assessment_topic')
            if assessment_topic_form.is_valid():
                assessment_topic_form.save()
                messages.success(request, 'Assessment topic created.')
                return redirect('content_manager')

        elif action == 'add_assessment_question':
            assessment_question_form = AssessmentQuestionForm(request.POST, prefix='assessment_question')
            if assessment_question_form.is_valid():
                assessment_question_form.save()
                messages.success(request, 'Assessment question created.')
                return redirect('content_manager')

        elif action == 'add_blog_post':
            blog_post_form = BlogPostForm(request.POST, request.FILES, prefix='blog_post')
            if blog_post_form.is_valid():
                post = blog_post_form.save(commit=False)
                post.author = request.user
                post.save()
                messages.success(request, 'Blog post created.')
                return redirect('content_manager')

        elif action == 'approve_comment':
            comment = BlogComment.objects.filter(id=request.POST.get('comment_id')).first()
            if comment:
                comment.approved = True
                comment.save(update_fields=['approved'])
                messages.success(request, 'Comment approved.')
                return redirect('content_manager')

    context = {
        'branding': branding,
        'branding_form': branding_form,
        'interview_category_form': interview_category_form,
        'interview_question_form': interview_question_form,
        'assessment_topic_form': assessment_topic_form,
        'assessment_question_form': assessment_question_form,
        'blog_post_form': blog_post_form,
        'recent_categories': Category.objects.order_by('order', 'name')[:8],
        'recent_questions': Question.objects.select_related('category').order_by('-id')[:8],
        'recent_topics': SkillTopic.objects.order_by('order', 'name')[:8],
        'recent_assessment_questions': SkillQuestion.objects.select_related('topic').order_by('-id')[:8],
        'recent_posts': BlogPost.objects.select_related('author').order_by('-created_at')[:8],
        'pending_comments': BlogComment.objects.filter(approved=False).select_related('user', 'post')[:8],
    }
    return render(request, 'dashboard/content_manager.html', context)


@login_required
def roadmap(request):
    resume_built = request.session.get('resume_built', False)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    context = build_user_roadmap(request.user, resume_built=resume_built, profile=profile)
    return render(request, 'dashboard/roadmap.html', context)
