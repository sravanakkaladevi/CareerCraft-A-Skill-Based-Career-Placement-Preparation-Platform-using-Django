from django.urls import path
from . import views

urlpatterns = [
    path('', views.assessment_home, name='assessment_home'),
    path('start/<int:topic_id>/', views.start_assessment, name='start_assessment'),
    path('question/<int:question_no>/', views.assess_question, name='assess_question'),
    path('result/', views.assess_result, name='assess_result'),
]