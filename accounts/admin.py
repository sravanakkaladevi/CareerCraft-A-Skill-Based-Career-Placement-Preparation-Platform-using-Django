from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'target_role', 'target_domain', 'experience_level', 'has_pending_role_change', 'theme_color']
    search_fields = ['user__username', 'user__email']
