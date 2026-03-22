from django.contrib import admin

from .models import BlogComment, BlogPost, Language, Lesson, Topic


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ["name", "icon", "order"]
    search_fields = ["name", "description"]
    fields = [
        "name",
        "icon",
        "description",
        "color",
        "tutorial_url",
        "cheatsheet_url",
        "practice_url",
        "order",
    ]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ["title", "language", "level", "order"]
    list_filter = ["language", "level"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "topic", "order"]
    list_filter = ["topic__language"]


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "author", "published", "created_at"]
    list_filter = ["category", "published"]
    search_fields = ["title", "summary", "content"]
    list_editable = ["published"]
    autocomplete_fields = ["author"]


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "approved", "created_at"]
    list_filter = ["approved", "created_at", "post"]
    search_fields = ["user__username", "post__title", "content"]
    list_editable = ["approved"]
