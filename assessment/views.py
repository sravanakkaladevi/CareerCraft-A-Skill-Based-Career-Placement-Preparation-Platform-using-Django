from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def assessment_home(request):
    return render(request, 'assessment/assessment.html')