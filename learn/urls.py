from django.urls import path
from . import views

urlpatterns = [
    path('', views.learn_home, name='learn_home'),
    path('language/<int:lang_id>/', views.language_topics, name='language_topics'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('blog/', views.blog_home, name='blog_home'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('blog/comment/<int:comment_id>/<str:value>/', views.react_to_comment, name='react_to_comment'),
]
