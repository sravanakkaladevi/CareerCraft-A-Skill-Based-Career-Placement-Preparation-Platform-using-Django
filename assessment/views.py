from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import UserProfile
from accounts.personalization import filter_project_domains_for_profile, get_profile_summary


PROJECT_DOMAINS = [
    {
        "name": "Web",
        "description": "Full-stack web products that are easier to demo in placements, internships, and final-year reviews.",
        "ideas": [
            {
                "name": "AI-Powered E-Commerce with Recommendation Engine",
                "subdomain": "Full-Stack",
                "language": "Python",
                "tools": "Django, React, Redis, Celery, Stripe API, ElasticSearch",
                "database": "PostgreSQL",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/justdjango/django-react-ecommerce",
            },
            {
                "name": "Multi-Tenant SaaS Project Management Tool (Jira Clone)",
                "subdomain": "Full-Stack",
                "language": "JavaScript",
                "tools": "Next.js, Node.js, GraphQL, WebSocket, Docker",
                "database": "PostgreSQL",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/makeplane/plane",
            },
            {
                "name": "Real-Time Collaborative Document Editor (Notion Clone)",
                "subdomain": "Full-Stack",
                "language": "JavaScript",
                "tools": "Next.js, Yjs CRDT, WebSocket, Tiptap Editor",
                "database": "MongoDB",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/steven-tey/novel",
            },
        ],
    },
    {
        "name": "AI/ML",
        "description": "Resume-strong AI ideas with modern LLM, RAG, and product-oriented workflows.",
        "ideas": [
            {
                "name": "LLM-Powered Personal Research Assistant",
                "subdomain": "LLM / RAG",
                "language": "Python",
                "tools": "LangChain, OpenAI, ChromaDB, FastAPI, React",
                "database": "ChromaDB",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/langchain-ai/langchain",
            },
            {
                "name": "Document Q&A using RAG (PDF Chat)",
                "subdomain": "LLM / RAG",
                "language": "Python",
                "tools": "LangChain, OpenAI, FAISS, Streamlit",
                "database": "FAISS",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/topics/rag-pdf-chat",
            },
            {
                "name": "AI Code Generation & Explanation Tool",
                "subdomain": "LLM / Developer Tools",
                "language": "Python",
                "tools": "OpenAI API, FastAPI, React, CodeMirror",
                "database": "PostgreSQL",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/topics/ai-code-generator",
            },
        ],
    },
    {
        "name": "Data Science",
        "description": "Strong analytics and MLOps projects if you want to show data engineering plus model delivery.",
        "ideas": [
            {
                "name": "End-to-End MLOps Pipeline (CI/CD for ML)",
                "subdomain": "MLOps",
                "language": "Python",
                "tools": "MLflow, DVC, FastAPI, Docker, GitHub Actions",
                "database": "PostgreSQL",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/mlflow/mlflow",
            },
            {
                "name": "Realtime Fraud Detection Pipeline",
                "subdomain": "Big Data",
                "language": "Python",
                "tools": "Kafka, Spark Streaming, Scikit-learn, Grafana",
                "database": "Cassandra",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/topics/fraud-detection-realtime",
            },
            {
                "name": "Customer 360 Analytics Platform",
                "subdomain": "Analytics",
                "language": "Python",
                "tools": "Pandas, dbt, Airflow, Metabase, Snowflake",
                "database": "Snowflake",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/topics/customer-analytics",
            },
        ],
    },
    {
        "name": "Cloud",
        "description": "Cloud-native project ideas for DevOps, architecture, deployment, and production-readiness.",
        "ideas": [
            {
                "name": "Serverless Microservices E-Commerce Backend",
                "subdomain": "Serverless",
                "language": "Python",
                "tools": "AWS Lambda, API Gateway, DynamoDB, CDK",
                "database": "DynamoDB",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/localstack-samples/sample-serverless-shopping-cart-apigateway-lambda-cognito",
            },
            {
                "name": "Multi-Region Fault-Tolerant Web App",
                "subdomain": "Cloud Architecture",
                "language": "Java",
                "tools": "Spring Boot, AWS Route53, RDS Multi-AZ, ELB",
                "database": "RDS",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/topics/multi-region-aws",
            },
            {
                "name": "Kubernetes-Native CI/CD Platform",
                "subdomain": "DevOps",
                "language": "Python",
                "tools": "K8s, ArgoCD, Helm, GitHub Actions, Prometheus",
                "database": "PostgreSQL",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/argoproj/argo-cd",
            },
        ],
    },
    {
        "name": "Cybersecurity",
        "description": "High-signal security projects with monitoring, automation, and zero-trust style system design.",
        "ideas": [
            {
                "name": "AI-Powered SIEM System",
                "subdomain": "SOC / AI",
                "language": "Python",
                "tools": "ELK Stack, ML, Kafka, React, Sigma Rules",
                "database": "Elasticsearch",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/Keyvanhardani/AI-Driven-SIEM-Realtime-Operator-with-Groq-Integration",
            },
            {
                "name": "Zero Trust Network Access Implementation",
                "subdomain": "Network Security",
                "language": "Python",
                "tools": "WireGuard, FastAPI, JWT, React, Docker",
                "database": "PostgreSQL",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/topics/zero-trust-network",
            },
            {
                "name": "Automated Penetration Testing Framework",
                "subdomain": "Pen Testing",
                "language": "Python",
                "tools": "Nmap, Metasploit API, FastAPI, React",
                "database": "PostgreSQL",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/topics/automated-pentest",
            },
        ],
    },
    {
        "name": "Android",
        "description": "Modern mobile ideas using AI, AR, and device capabilities that feel stronger than basic CRUD apps.",
        "ideas": [
            {
                "name": "AI-Powered Personal Diary with Emotion Tracking",
                "subdomain": "Mobile / AI",
                "language": "Kotlin",
                "tools": "Jetpack Compose, ML Kit, Room DB, TFLite",
                "database": "Room DB",
                "difficulty": "Hard",
                "impact": "★★★★",
                "github": "github.com/rektplorer64/ITCS424-PJ_Diaryly",
            },
            {
                "name": "Augmented Reality Campus Navigation",
                "subdomain": "AR / Mobile",
                "language": "Kotlin",
                "tools": "ARCore, Google Maps SDK, Jetpack Compose",
                "database": "Firebase",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/topics/ar-navigation-android",
            },
            {
                "name": "Real-Time Language Translator with Camera",
                "subdomain": "Mobile / AI",
                "language": "Kotlin",
                "tools": "ML Kit Text Recognition, CameraX, TFLite",
                "database": "Room DB",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/topics/realtime-translation-android",
            },
        ],
    },
    {
        "name": "EdTech",
        "description": "Education-focused builds that fit your platform theme and are easy to explain in placements.",
        "ideas": [
            {
                "name": "Adaptive Learning Engine for GATE/UPSC",
                "subdomain": "EdTech AI",
                "language": "Python",
                "tools": "IRT, Django, React, Gamification, NLP",
                "database": "PostgreSQL",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/topics/adaptive-learning",
            },
            {
                "name": "AI-Powered Code Plagiarism Detector",
                "subdomain": "EdTech AI",
                "language": "Python",
                "tools": "AST Comparison, ML, FastAPI, React",
                "database": "PostgreSQL",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/topics/code-plagiarism-detection",
            },
            {
                "name": "Virtual Lab Simulator for Chemistry/Physics",
                "subdomain": "EdTech",
                "language": "JavaScript",
                "tools": "Three.js, React, Physics Engine, WebGL",
                "database": "MongoDB",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/topics/virtual-lab",
            },
        ],
    },
    {
        "name": "CareerTech",
        "description": "Projects aligned with resume building, skill mapping, and career planning, which fits CareerCraft especially well.",
        "ideas": [
            {
                "name": "AI Career Path Advisor",
                "subdomain": "AI / Career",
                "language": "Python",
                "tools": "LangChain, OpenAI, FastAPI, React",
                "database": "PostgreSQL",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/topics/career-advisor-ai",
            },
            {
                "name": "Skill Gap Analyzer for IT Professionals",
                "subdomain": "Analytics",
                "language": "Python",
                "tools": "NLP, Pandas, FastAPI, React, LinkedIn API",
                "database": "PostgreSQL",
                "difficulty": "Hard",
                "impact": "★★★★★",
                "github": "github.com/topics/skill-gap-analysis",
            },
            {
                "name": "Developer Portfolio Auto-Generator from GitHub",
                "subdomain": "Full-Stack",
                "language": "JavaScript",
                "tools": "GitHub API, Next.js, OpenAI, Vercel",
                "database": "PostgreSQL",
                "difficulty": "Medium",
                "impact": "★★★★★",
                "github": "github.com/topics/portfolio-generator",
            },
        ],
    },
]


def _github_url(value):
    if not value:
        return ""
    if value.startswith(("http://", "https://")):
        return value
    return f"https://{value}"


def _idea_summary(idea):
    return (
        f"{idea['subdomain']} project using {idea['language']} with {idea['difficulty'].lower()} "
        f"difficulty and {idea['impact']} resume impact."
    )


@login_required
def assessment_home(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    personalized_domains = filter_project_domains_for_profile(PROJECT_DOMAINS, profile)
    featured_projects = []
    total_ideas = 0

    for domain in personalized_domains:
        for idea in domain["ideas"]:
            idea["github_url"] = _github_url(idea["github"])
            idea["summary"] = _idea_summary(idea)
        total_ideas += len(domain["ideas"])
        featured_projects.append(
            {
                "name": domain["ideas"][0]["name"],
                "role": f"{domain['name']} Projects",
                "domain": domain["description"],
                "summary": domain["ideas"][0]["summary"],
                "stack": domain["ideas"][0]["tools"],
                "highlights": [
                    f"Language: {domain['ideas'][0]['language']}",
                    f"Database: {domain['ideas'][0]['database']}",
                ],
                "references": [
                    {"label": "GitHub Reference", "url": domain["ideas"][0]["github_url"]},
                ],
            }
        )

    return render(
        request,
        "assessment/assessment.html",
        {
            "top_projects": featured_projects[:6],
            "project_domains": personalized_domains,
            "project_count": total_ideas,
            "domain_count": len(personalized_domains),
            "profile_summary": get_profile_summary(profile),
            "target_role_label": profile.get_target_role_display() if profile.target_role else "Student",
            "target_domain_label": profile.get_target_domain_display() if profile.target_domain else "All domains",
            "profile_complete": profile.is_profile_complete,
        },
    )


@login_required
def start_assessment(request, topic_id):
    for key in ["assess_questions", "assess_topic", "assess_answers"]:
        request.session.pop(key, None)
    return redirect("assessment_home")


@login_required
def assess_question(request, question_no):
    for key in ["assess_questions", "assess_topic", "assess_answers"]:
        request.session.pop(key, None)
    return redirect("assessment_home")


@login_required
def assess_result(request):
    for key in ["assess_questions", "assess_topic", "assess_answers"]:
        request.session.pop(key, None)
    return redirect("assessment_home")
