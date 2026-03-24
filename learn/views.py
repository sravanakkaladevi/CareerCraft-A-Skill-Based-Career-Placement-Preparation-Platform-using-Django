from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from accounts.models import UserProfile
from accounts.personalization import filter_languages_for_profile, get_profile_summary
from .models import Language, Topic, Lesson, BlogPost, BlogComment, BlogCommentReaction


@login_required
def learn_home(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    languages = filter_languages_for_profile(Language.objects.all(), profile)
    return render(request, 'learn/learn_home.html', {
        'languages': languages,
        'profile_summary': get_profile_summary(profile),
        'target_role_label': profile.get_target_role_display() if profile.target_role else 'Student',
    })


@login_required
def language_topics(request, lang_id):
    language = get_object_or_404(Language, id=lang_id)
    topics = list(
        Topic.objects.filter(language=language)
        .prefetch_related(Prefetch('lesson_set', queryset=Lesson.objects.order_by('order', 'id')))
    )
    for topic in topics:
        topic.lessons = list(topic.lesson_set.all())
        topic.first_lesson = topic.lessons[0] if topic.lessons else None
        topic.lesson_count = len(topic.lessons)

    beginner = [topic for topic in topics if topic.level == 'beginner']
    intermediate = [topic for topic in topics if topic.level == 'intermediate']
    advanced = [topic for topic in topics if topic.level == 'advanced']
    topic_groups = [
        {"title": "Beginner", "items": beginner},
        {"title": "Intermediate", "items": intermediate},
        {"title": "Advanced", "items": advanced},
    ]

    total_lessons = sum(topic.lesson_count for topic in topics)
    total_topics = len(topics)
    first_topic_with_lesson = next((topic for topic in topics if topic.first_lesson), None)
    return render(request, 'learn/language_topics.html', {
        'language': language,
        'beginner': beginner,
        'intermediate': intermediate,
        'advanced': advanced,
        'topic_groups': topic_groups,
        'total_topics': total_topics,
        'total_lessons': total_lessons,
        'first_topic_with_lesson': first_topic_with_lesson,
    })


@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    topic = lesson.topic
    language = topic.language
    all_lessons = Lesson.objects.filter(topic=topic)
    current_index = list(all_lessons).index(lesson)
    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None

    language_topics = list(
        Topic.objects.filter(language=language)
        .prefetch_related(
            Prefetch(
                'lesson_set',
                queryset=Lesson.objects.order_by('order', 'id').prefetch_related('lesson_images'),
            )
        )
    )
    total_language_lessons = 0
    current_topic_position = 0
    for idx, language_topic in enumerate(language_topics, 1):
        language_topic.lessons = list(language_topic.lesson_set.all())
        language_topic.lesson_count = len(language_topic.lessons)
        total_language_lessons += language_topic.lesson_count
        if language_topic.id == topic.id:
            current_topic_position = idx

    return render(request, 'learn/lesson.html', {
        'lesson': lesson,
        'topic': topic,
        'language': language,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'all_lessons': all_lessons,
        'current_index': current_index,
        'language_topics': language_topics,
        'total_language_lessons': total_language_lessons,
        'total_language_topics': len(language_topics),
        'current_topic_position': current_topic_position,
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
                approved=True,
            )
            messages.success(request, 'Comment added successfully.')
        else:
            messages.error(request, 'Please write a comment before submitting.')
        return redirect('blog_detail', post_id=post.id)

    comments = list(post.comments.filter(approved=True).select_related('user').prefetch_related('reactions'))
    user_reactions = {
        reaction.comment_id: reaction.value
        for reaction in BlogCommentReaction.objects.filter(comment__in=comments, user=request.user)
    }
    for comment in comments:
        comment.user_reaction = user_reactions.get(comment.id, 0)
    pending_comments = post.comments.filter(approved=False).select_related('user') if request.user.is_superuser else []
    return render(request, 'learn/blog_detail.html', {
        'post': post,
        'related': related,
        'comments': comments,
        'pending_comments': pending_comments,
    })


@login_required
def react_to_comment(request, comment_id, value):
    if request.method != 'POST' or value not in {"like", "dislike"}:
        return redirect('blog_home')

    comment = get_object_or_404(BlogComment.objects.select_related("post"), id=comment_id, approved=True)
    numeric_value = 1 if value == "like" else -1

    reaction, created = BlogCommentReaction.objects.get_or_create(
        comment=comment,
        user=request.user,
        defaults={"value": numeric_value},
    )

    if not created:
        if reaction.value == numeric_value:
            reaction.delete()
        else:
            reaction.value = numeric_value
            reaction.save(update_fields=["value"])

    return redirect('blog_detail', post_id=comment.post_id)
