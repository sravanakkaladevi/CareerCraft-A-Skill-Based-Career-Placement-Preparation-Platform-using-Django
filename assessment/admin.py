from django.contrib import admin
from .models import SkillTopic, SkillQuestion, SkillScore

@admin.register(SkillTopic)
class SkillTopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order']

@admin.register(SkillQuestion)
class SkillQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'topic', 'correct_option', 'difficulty']
    list_filter = ['topic', 'difficulty']

@admin.register(SkillScore)
class SkillScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'topic', 'percentage', 'assessed_at']