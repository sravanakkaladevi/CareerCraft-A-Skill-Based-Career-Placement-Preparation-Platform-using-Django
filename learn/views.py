from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Language, Topic, Lesson, BlogPost


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
    posts = BlogPost.objects.filter(published=True)
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
    post = get_object_or_404(BlogPost, id=post_id, published=True)
    related = BlogPost.objects.filter(
        published=True, category=post.category
    ).exclude(id=post.id)[:3]
    return render(request, 'learn/blog_detail.html', {
        'post': post,
        'related': related,
    })