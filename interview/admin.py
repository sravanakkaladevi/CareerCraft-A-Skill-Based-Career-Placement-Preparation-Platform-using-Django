from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, MockResult, Question


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        help_texts = {
            "logo_image": "Upload a custom logo image for this category.",
            "logo_url": "Optional direct image URL. Uploaded image takes priority over URL.",
            "icon": "Optional short fallback text or emoji. If left blank, built-in logos are used for standard names like Python, Django, Web Dev, DSA, DBMS, Operating Systems, Computer Networks, OOPS, HR Questions, Aptitude, and System Design.",
        }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ["name", "icon_preview", "order"]
    ordering = ["order", "name"]
    search_fields = ["name", "description"]
    readonly_fields = ["icon_preview", "icon_guide"]
    fields = [
        "name",
        "description",
        "order",
        "logo_image",
        "logo_url",
        "icon",
        "icon_preview",
        "icon_guide",
    ]

    def icon_preview(self, obj):
        if obj.pk:
            from .views import _display_icon

            return mark_safe(
                f'<div style="width:58px;height:58px;display:flex;align-items:center;justify-content:center;border:1px solid #dbe5ef;border-radius:14px;background:#fff;color:#7c3aed;overflow:hidden;padding:6px;">{_display_icon(obj)}</div>'
            )
        return "Save category to preview icon"

    icon_preview.short_description = "Current icon"

    def icon_guide(self, obj):
        return mark_safe(
            "<div style='line-height:1.7;'>"
            "<strong>Built-in category logos:</strong> Python, DSA, Web Dev, Django, DBMS, Operating Systems, Computer Networks, OOPS, System Design, HR Questions, Aptitude."
            "<br><strong>Priority:</strong> uploaded image -> image URL -> built-in logo -> icon text."
            "<br><strong>Tip:</strong> keep the category name matching one of these to get the default logo automatically."
            "</div>"
        )

    icon_guide.short_description = "Logo guide"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "category", "correct_option", "difficulty"]
    list_filter = ["category", "difficulty"]
    search_fields = [
        "question_text",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "explanation",
    ]


@admin.register(MockResult)
class MockResultAdmin(admin.ModelAdmin):
    list_display = ["user", "category", "percentage", "taken_at"]
    list_filter = ["category", "taken_at"]
    search_fields = ["user__username", "category__name"]
