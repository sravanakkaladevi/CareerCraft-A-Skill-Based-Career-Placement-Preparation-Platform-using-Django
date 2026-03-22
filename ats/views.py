from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services.ats_engine import analyze_resume
from .services.pdf_parser import extract_text_from_pdf


@login_required
def ats_view(request):
    if request.method == "POST":
        job_description = request.POST.get("job_description", "")
        resume_text = request.POST.get("resume", "")
        resume_file = request.FILES.get("resume_file")

        if resume_file:
            extracted_text = extract_text_from_pdf(resume_file)
            if not extracted_text:
                return render(
                    request,
                    "ats/form.html",
                    {
                        "error": "Could not extract text from PDF. Please upload a text-based PDF or paste resume text.",
                        "job_description": job_description,
                        "resume": resume_text,
                    },
                )
            resume_text = extracted_text

        result = analyze_resume(resume_text, job_description)
        return render(
            request,
            "ats/result.html",
            {
                "result": result,
                "debug": result.get("debug", {}),
                "job_description": job_description,
                "resume": request.POST.get("resume", ""),
            },
        )

    return render(request, "ats/form.html")
