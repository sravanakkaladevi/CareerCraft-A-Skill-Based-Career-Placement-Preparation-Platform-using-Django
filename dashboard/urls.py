from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('content-manager/', views.content_manager, name='content_manager'),
    path('roadmap/', views.roadmap, name='roadmap'),
]
