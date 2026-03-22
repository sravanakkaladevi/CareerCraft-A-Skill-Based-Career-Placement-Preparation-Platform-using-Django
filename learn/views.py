from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Language, Topic, Lesson, BlogPost, BlogComment


@login_required
def learn_home(request):
    languages = Language.objects.all()
    return render(request, 'learn/learn_home.html', {
        'languages': languages,
    })


@login_required
def language_topics(request, lang_id):
    language = get_object_or_404(Language, id=lang_id)
    topics = Topic.objects.filter(language=language)
    beginner = topics.filter(level='beginner')
    intermediate = topics.filter(level='intermediate')
    advanced = topics.filter(level='advanced')
    return render(request, 'learn/language_topics.html', {
        'language': language,
        'beginner': beginner,
        'intermediate': intermediate,
        'advanced': advanced,
    })


@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    topic = lesson.topic
    all_lessons = Lesson.objects.filter(topic=topic)
    current_index = list(all_lessons).index(lesson)
    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None
    return render(request, 'learn/lesson.html', {
        'lesson': lesson,
        'topic': topic,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'all_lessons': all_lessons,
        'current_index': current_index,
    })


@login_required
def blog_home(request):
    category = request.GET.get('cat', '')
    posts = BlogPost.objects.all() if request.user.is_superuser else BlogPost.objects.filter(published=True)
    if category:
        posts = posts.filter(category=category)
    categories = BlogPost.CATEGORY
    return render(request, 'learn/blog_home.html', {
        'posts': posts,
        'categories': categories,
        'active_cat': category,
    })


@login_required
def blog_detail(request, post_id):
    if request.user.is_superuser:
        post = get_object_or_404(BlogPost, id=post_id)
        related = BlogPost.objects.filter(category=post.category).exclude(id=post.id)[:3]
    else:
        post = get_object_or_404(BlogPost, id=post_id, published=True)
        related = BlogPost.objects.filter(published=True, category=post.category).exclude(id=post.id)[:3]

    if request.method == 'POST':
        comment_text = request.POST.get('comment', '').strip()
        if comment_text:
            BlogComment.objects.create(
                post=post,
                user=request.user,
                content=comment_text,
                approved=request.user.is_superuser,
            )
            if request.user.is_superuser:
                messages.success(request, 'Comment added and approved.')
            else:
                messages.success(request, 'Comment submitted. It will appear after admin approval.')
        else:
            messages.error(request, 'Please write a comment before submitting.')
        return redirect('blog_detail', post_id=post.id)

    comments = post.comments.filter(approved=True).select_related('user')
    pending_comments = post.comments.filter(approved=False).select_related('user') if request.user.is_superuser else []
    return render(request, 'learn/blog_detail.html', {
        'post': post,
        'related': related,
        'comments': comments,
        'pending_comments': pending_comments,
    })
