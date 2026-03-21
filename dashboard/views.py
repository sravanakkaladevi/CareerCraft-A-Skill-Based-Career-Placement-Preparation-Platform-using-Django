from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard/dashboard.html')

def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_superuser:
        return redirect('dashboard')
    
    total_users = User.objects.filter(is_superuser=False).count()
    recent_users = User.objects.filter(is_superuser=False).order_by('-date_joined')[:10]
    
    context = {
        'total_users': total_users,
        'recent_users': recent_users,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)