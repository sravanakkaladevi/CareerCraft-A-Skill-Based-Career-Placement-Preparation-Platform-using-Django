from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

handler404 = 'careercraft.views.custom_404'

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('resume/', include('resume.urls')),
    path('interview/', include('interview.urls')),
    path('assessment/', include('assessment.urls')),
    path('learn/', include('learn.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)