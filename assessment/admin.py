from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import SkillQuestion, SkillScore, SkillTopic


class SkillTopicAdminForm(forms.ModelForm):
    class Meta:
        model = SkillTopic
        fields = "__all__"
        help_texts = {
            "logo_image": "Upload a custom logo image for this assessment topic.",
            "logo_url": "Optional direct image URL. Uploaded image takes priority over URL.",
            "icon": "Short fallback text if no custom logo is provided.",
        }


@admin.register(SkillTopic)
class SkillTopicAdmin(admin.ModelAdmin):
    form = SkillTopicAdminForm
    list_display = ["name", "logo_preview", "question_total", "order"]
    ordering = ["order", "name"]
    search_fields = ["name"]
    readonly_fields = ["logo_preview"]
    fields = ["name", "icon", "logo_image", "logo_url", "logo_preview", "order"]

    def logo_preview(self, obj):
        if obj.logo_image:
            return mark_safe(f'<img src="{obj.logo_image.url}" alt="{obj.name}" style="width:52px;height:52px;object-fit:cover;border-radius:14px;border:1px solid #dbe5ef;">')
        if obj.logo_url:
            return mark_safe(f'<img src="{obj.logo_url}" alt="{obj.name}" style="width:52px;height:52px;object-fit:cover;border-radius:14px;border:1px solid #dbe5ef;">')
        return mark_safe(
            f'<div style="width:52px;height:52px;border-radius:14px;border:1px solid #dbe5ef;display:flex;align-items:center;justify-content:center;background:#eef6ff;color:#185FA5;font-weight:700;">{obj.icon}</div>'
        )

    logo_preview.short_description = "Preview"

    def question_total(self, obj):
        return obj.skillquestion_set.count()

    question_total.short_description = "Questions"


@admin.register(SkillQuestion)
class SkillQuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "topic", "correct_option", "difficulty"]
    list_filter = ["topic", "difficulty"]
    autocomplete_fields = ["topic"]
    search_fields = ["question_text", "option_a", "option_b", "option_c", "option_d", "explanation"]


@admin.register(SkillScore)
class SkillScoreAdmin(admin.ModelAdmin):
    list_display = ["user", "topic", "percentage", "assessed_at"]
