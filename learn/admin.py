from django.contrib import admin

from .models import BlogComment, BlogCommentReaction, BlogPost, Language, Lesson, LessonImage, Topic


class LessonImageInline(admin.TabularInline):
    model = LessonImage
    extra = 1
    fields = ["image", "caption", "alignment", "order"]


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
    search_fields = ["title", "summary", "language__name"]
    fields = [
        "language",
        "title",
        "summary",
        "cover_image",
        "level",
        "order",
    ]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "topic", "order"]
    list_filter = ["topic__language"]
    search_fields = ["title", "theory", "practice_note", "topic__title", "topic__language__name"]
    inlines = [LessonImageInline]
    fields = [
        "topic",
        "title",
        "theory",
        "content_image",
        "image_caption",
        "syntax_example",
        "practice_note",
        "order",
    ]


@admin.register(LessonImage)
class LessonImageAdmin(admin.ModelAdmin):
    list_display = ["lesson", "alignment", "order"]
    list_filter = ["lesson__topic__language", "alignment"]
    search_fields = ["lesson__title", "caption", "lesson__topic__title"]


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


@admin.register(BlogCommentReaction)
class BlogCommentReactionAdmin(admin.ModelAdmin):
    list_display = ["user", "comment", "value", "created_at"]
    list_filter = ["value", "created_at", "comment__post"]
    search_fields = ["user__username", "comment__post__title", "comment__content"]
