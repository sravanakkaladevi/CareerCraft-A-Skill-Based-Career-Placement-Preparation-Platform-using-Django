import re
import io
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def ats_score(resume_text, job_description):
    resume_words = set(resume_text.lower().split())
    jd_keywords = set(re.findall(r'\b\w+\b', job_description.lower()))
    stopwords = {
        'the','and','or','is','in','a','to','for','of','with','on','at',
        'be','are','was','were','this','that','have','has','by','as','an',
        'it','its','we','you','your','our','will','can','may','from','into',
        'about','up','also','but','not','they','their','which','when','who','how'
    }
    jd_keywords -= stopwords
    matched = resume_words & jd_keywords
    score = int((len(matched) / len(jd_keywords)) * 100) if jd_keywords else 0
    missing = list(jd_keywords - resume_words)[:15]
    return score, missing, list(matched)[:15]


@login_required
def resume_home(request):
    context = {}
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        linkedin = request.POST.get('linkedin', '')
        github = request.POST.get('github', '')
        portfolio = request.POST.get('portfolio', '')
        summary = request.POST.get('summary', '')
        skills_programming = request.POST.get('skills_programming', '')
        skills_web = request.POST.get('skills_web', '')
        skills_backend = request.POST.get('skills_backend', '')
        skills_db = request.POST.get('skills_db', '')
        skills_tools = request.POST.get('skills_tools', '')
        skills_other = request.POST.get('skills_other', '')

        skills_list = []
        if skills_programming:
            skills_list.append(f'Programming: {skills_programming}')
        if skills_web:
            skills_list.append(f'Web: {skills_web}')
        if skills_backend:
            skills_list.append(f'Backend: {skills_backend}')
        if skills_db:
            skills_list.append(f'Database: {skills_db}')
        if skills_tools:
            skills_list.append(f'Tools: {skills_tools}')
        if skills_other:
            skills_list.append(f'Other: {skills_other}')

        project_titles = request.POST.getlist('project_title[]')
        project_techs = request.POST.getlist('project_tech[]')
        project_githubs = request.POST.getlist('project_github[]')
        project_descs = request.POST.getlist('project_desc[]')

        projects_list = []
        for i in range(len(project_titles)):
            if project_titles[i].strip():
                points = [p.strip() for p in project_descs[i].split('\n') if p.strip()] if i < len(project_descs) else []
                projects_list.append({
                    'title': project_titles[i],
                    'tech': project_techs[i] if i < len(project_techs) else '',
                    'github': project_githubs[i] if i < len(project_githubs) else '',
                    'points': points,
                })

        exp_roles = request.POST.getlist('exp_role[]')
        exp_durations = request.POST.getlist('exp_duration[]')
        exp_orgs = request.POST.getlist('exp_org[]')
        exp_locations = request.POST.getlist('exp_location[]')
        exp_descs = request.POST.getlist('exp_desc[]')

        experience_list = []
        for i in range(len(exp_roles)):
            if exp_roles[i].strip():
                points = [p.strip() for p in exp_descs[i].split('\n') if p.strip()] if i < len(exp_descs) else []
                experience_list.append({
                    'role': exp_roles[i],
                    'duration': exp_durations[i] if i < len(exp_durations) else '',
                    'org': exp_orgs[i] if i < len(exp_orgs) else '',
                    'location': exp_locations[i] if i < len(exp_locations) else '',
                    'points': points,
                })

        edu_degrees = request.POST.getlist('edu_degree[]')
        edu_years = request.POST.getlist('edu_year[]')
        edu_colleges = request.POST.getlist('edu_college[]')
        edu_grades = request.POST.getlist('edu_grade[]')

        education_list = []
        for i in range(len(edu_degrees)):
            if edu_degrees[i].strip():
                education_list.append({
                    'degree': edu_degrees[i],
                    'year': edu_years[i] if i < len(edu_years) else '',
                    'college': edu_colleges[i] if i < len(edu_colleges) else '',
                    'grade': edu_grades[i] if i < len(edu_grades) else '',
                })

        context = {
            'submitted': True,
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'linkedin': linkedin,
            'github': github,
            'portfolio': portfolio,
            'summary': summary,
            'skills_programming': skills_programming,
            'skills_web': skills_web,
            'skills_backend': skills_backend,
            'skills_db': skills_db,
            'skills_tools': skills_tools,
            'skills_other': skills_other,
            'skills_list': skills_list,
            'projects_list': projects_list,
            'experience_list': experience_list,
            'education_list': education_list,
            'projects_json': json.dumps(projects_list),
            'experience_json': json.dumps(experience_list),
            'education_json': json.dumps(education_list),
        }

    return render(request, 'resume/resume.html', context)


@login_required
def download_pdf(request):
    if request.method == 'POST':
        from weasyprint import HTML
        from django.template.loader import render_to_string

        full_name = request.POST.get('full_name', '')
        skills_list = []
        for key, label in [
            ('skills_programming', 'Programming'),
            ('skills_web', 'Web'),
            ('skills_backend', 'Backend'),
            ('skills_db', 'Database'),
            ('skills_tools', 'Tools'),
            ('skills_other', 'Other'),
        ]:
            val = request.POST.get(key, '')
            if val:
                skills_list.append(f'{label}: {val}')

        projects_list = json.loads(request.POST.get('projects_json', '[]'))
        experience_list = json.loads(request.POST.get('experience_json', '[]'))
        education_list = json.loads(request.POST.get('education_json', '[]'))

        context = {
            'full_name': full_name,
            'email': request.POST.get('email', ''),
            'phone': request.POST.get('phone', ''),
            'linkedin': request.POST.get('linkedin', ''),
            'github': request.POST.get('github', ''),
            'portfolio': request.POST.get('portfolio', ''),
            'summary': request.POST.get('summary', ''),
            'skills': True,
            'skills_list': skills_list,
            'projects': bool(projects_list),
            'projects_list': projects_list,
            'experience': bool(experience_list),
            'experience_list': experience_list,
            'education': bool(education_list),
            'education_list': education_list,
        }

        html_string = render_to_string('resume/resume_pdf.html', context)
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        safe_name = re.sub(r'[^\w\s-]', '', full_name).strip().replace(' ', '_')
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{safe_name}_Resume.pdf"'
        return response

    return redirect('resume_home')


@login_required
def ats_analyzer(request):
    context = {}
    if request.method == 'POST':
        job_description = request.POST.get('job_description', '')
        resume_file = request.FILES.get('resume_file')
        resume_text_input = request.POST.get('resume_text', '')

        if resume_file:
            try:
                from pdfminer.high_level import extract_text
                pdf_bytes = resume_file.read()
                resume_text = extract_text(io.BytesIO(pdf_bytes))
            except Exception:
                resume_text = resume_text_input
        else:
            resume_text = resume_text_input

        if resume_text and job_description:
            score, missing, matched = ats_score(resume_text, job_description)
            if score >= 70:
                score_color = 'green'
                score_msg = 'Strong match'
            elif score >= 40:
                score_color = 'amber'
                score_msg = 'Moderate match — improve keywords'
            else:
                score_color = 'red'
                score_msg = 'Weak match — add missing keywords'

            context = {
                'score': score,
                'score_color': score_color,
                'score_msg': score_msg,
                'missing': missing,
                'matched': matched,
                'job_description': job_description,
                'analyzed': True,
            }
        else:
            context['error'] = 'Please provide both resume content and job description'

    return render(request, 'resume/ats.html', context)