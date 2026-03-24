from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from dashboard.models import SiteBranding
from .personalization import (
    apply_profile_inputs,
    get_profile_change_request_summary,
    get_profile_change_status_meta,
    get_profile_setup_choices,
    queue_profile_change,
)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if request.user.is_authenticated:
            logout(request)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html', {
        'show_switch_notice': request.user.is_authenticated,
        **get_profile_setup_choices(),
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'accounts/login.html', get_profile_setup_choices())
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/login.html', get_profile_setup_choices())
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        profile, _ = UserProfile.objects.get_or_create(user=user)
        apply_profile_inputs(profile, request.POST)
        profile.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'accounts/login.html', get_profile_setup_choices())


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    branding = SiteBranding.get_solo() if request.user.is_superuser else None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_profile':
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            theme_color = request.POST.get('theme_color', '#185FA5').strip() or '#185FA5'
            uploaded_image = request.FILES.get('profile_image')
            if username and username != request.user.username:
                if User.objects.filter(username=username).exclude(id=request.user.id).exists():
                    messages.error(request, 'Username already taken')
                else:
                    request.user.username = username
                    request.user.save()
                    messages.success(request, 'Profile updated successfully')
            if email and email != request.user.email:
                request.user.email = email
                request.user.save()
                messages.success(request, 'Email updated successfully')
            profile.theme_color = theme_color
            incoming_role = (request.POST.get('target_role') or '').strip()
            incoming_domain = profile.target_domain
            requested_role = (request.POST.get('target_role') or '').strip()
            requested_domain = {
                'frontend': 'web',
                'backend': 'web',
                'fullstack': 'web',
                'data': 'data_science',
                'ai_ml': 'ai_ml',
                'devops': 'cloud',
                'cybersecurity': 'cybersecurity',
                'mobile': 'android',
            }.get(requested_role, '')
            incoming_experience = (request.POST.get('experience_level') or 'fresher').strip() or 'fresher'
            role_changed = (
                incoming_role != profile.target_role
                or requested_domain != profile.target_domain
                or incoming_experience != profile.experience_level
            )
            if request.user.is_superuser or not profile.is_profile_complete:
                apply_profile_inputs(profile, request.POST)
                profile.role_change_status = ''
                profile.role_change_requested_at = None
                profile.role_change_reviewed_at = None
                profile.pending_target_role = ''
                profile.pending_target_domain = ''
                profile.pending_experience_level = ''
            elif role_changed:
                queue_profile_change(profile, request.POST)
                messages.info(request, 'Role change request sent to admin for approval.')
            if uploaded_image:
                profile.profile_image = uploaded_image
            if request.user.is_superuser and branding:
                branding.admin_primary_color = request.POST.get('admin_primary_color', branding.admin_primary_color).strip() or branding.admin_primary_color
                branding.admin_accent_color = request.POST.get('admin_accent_color', branding.admin_accent_color).strip() or branding.admin_accent_color
                branding.admin_background_color = request.POST.get('admin_background_color', branding.admin_background_color).strip() or branding.admin_background_color
                branding.admin_surface_color = request.POST.get('admin_surface_color', branding.admin_surface_color).strip() or branding.admin_surface_color
                branding.save()
                messages.success(request, 'Admin theme updated successfully')
            profile.save()
            messages.success(request, 'Profile updated successfully')

        elif action == 'change_password':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if not request.user.check_password(old_password):
                messages.error(request, 'Current password is incorrect')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match')
            elif len(new_password) < 6:
                messages.error(request, 'Password must be at least 6 characters')
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully')

    return render(request, 'accounts/profile.html', {
        'user_profile': profile,
        'site_branding': branding,
        'pending_profile_change_summary': get_profile_change_request_summary(profile),
        'profile_change_status_meta': get_profile_change_status_meta(profile),
        **get_profile_setup_choices(),
    })
