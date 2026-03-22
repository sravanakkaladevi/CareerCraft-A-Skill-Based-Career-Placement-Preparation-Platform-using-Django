from django.contrib import admin
from .models import Language, Topic, Lesson, BlogPost


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'level', 'order']
    list_filter = ['language', 'level']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'order']
    list_filter = ['topic__language']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'published', 'created_at']
    list_filter = ['category', 'published']
    search_fields = ['title', 'content']