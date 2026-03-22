from .models import UserProfile


def user_preferences(request):
    if not request.user.is_authenticated:
        return {}

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return {
        'user_profile': profile,
        'active_theme_color': profile.theme_color or '#185FA5',
    }
