from django.urls import path
from . import views

urlpatterns = [
    path('', views.interview_home, name='interview_home'),
    path('start/<int:category_id>/', views.start_test, name='start_test'),
    path('question/<int:question_no>/', views.quiz_question, name='quiz_question'),
    path('result/', views.quiz_result, name='quiz_result'),
]