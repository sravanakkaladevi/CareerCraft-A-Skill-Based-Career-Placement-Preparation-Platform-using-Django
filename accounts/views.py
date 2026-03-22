from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile


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
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'accounts/login.html')
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        login(request, user)
        return redirect('dashboard')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

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
            if uploaded_image:
                profile.profile_image = uploaded_image
            profile.save()
            messages.success(request, 'Theme updated successfully')

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
    })
