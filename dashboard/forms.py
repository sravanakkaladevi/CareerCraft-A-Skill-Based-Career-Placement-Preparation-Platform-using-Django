from django import forms

from assessment.models import SkillQuestion, SkillTopic
from interview.models import Category, Question
from learn.models import BlogPost

from .models import SiteBranding


class SiteBrandingForm(forms.ModelForm):
    class Meta:
        model = SiteBranding
        fields = [
            "company_name",
            "tagline",
            "logo",
            "admin_primary_color",
            "admin_accent_color",
            "admin_background_color",
            "admin_surface_color",
        ]
        widgets = {
            "admin_primary_color": forms.TextInput(attrs={"type": "color"}),
            "admin_accent_color": forms.TextInput(attrs={"type": "color"}),
            "admin_background_color": forms.TextInput(attrs={"type": "color"}),
            "admin_surface_color": forms.TextInput(attrs={"type": "color"}),
        }


class InterviewCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "order", "logo_image", "logo_url", "icon"]


class InterviewQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "category",
            "difficulty",
            "question_text",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_option",
            "explanation",
        ]


class AssessmentTopicForm(forms.ModelForm):
    class Meta:
        model = SkillTopic
        fields = ["name", "icon", "logo_image", "logo_url", "order"]


class AssessmentQuestionForm(forms.ModelForm):
    class Meta:
        model = SkillQuestion
        fields = [
            "topic",
            "difficulty",
            "question_text",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_option",
            "explanation",
        ]


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "title",
            "category",
            "cover_image",
            "summary",
            "content",
            "published",
            "read_time",
        ]
