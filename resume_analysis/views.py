from django.shortcuts import render
from .ai import text_extractor, summarizer, skill_matcher, jd_comparator, langchain_flow
from django.conf import settings
import os
import re

INITIAL_DISPLAY = 3

ALL_JOBS = [
    {
        "title": "Python Developer",
        "company": "Tech Solutions",
        "description": "Work on AI projects",
        "location": "Remote",
        "experience_required": 2,
        "skills_required": ["Python", "Django", "Machine Learning"],
        "job_type": "remote",
        "degree_required": "Bachelors",
        "cgpa_required": 7.0
    },
    {
        "title": "Data Analyst",
        "company": "DataCorp",
        "description": "Analyze resumes and job data",
        "location": "Jaipur",
        "experience_required": 1,
        "skills_required": ["Python", "Excel", "Data Analysis"],
        "job_type": "fulltime",
        "degree_required": "Bachelors",
        "cgpa_required": 6.5
    },
    {
        "title": "Machine Learning Engineer",
        "company": "ML Innovations",
        "description": "Build ML models",
        "location": "Bangalore",
        "experience_required": 3,
        "skills_required": ["Python", "Machine Learning", "Data Science"],
        "job_type": "fulltime",
        "degree_required": "Masters",
        "cgpa_required": 7.5
    },
    {
        "title": "Full Stack Developer",
        "company": "WebWorks",
        "description": "Develop web applications",
        "location": "Jaipur",
        "experience_required": 1,
        "skills_required": ["Python", "Django", "JavaScript", "HTML", "CSS"],
        "job_type": "fulltime",
        "degree_required": "Bachelors",
        "cgpa_required": 6.5
    },
    {
        "title": "Business Analyst",
        "company": "BizAnalytics",
        "description": "Analyze business data",
        "location": "Remote",
        "experience_required": 2,
        "skills_required": ["Excel", "SQL", "Power BI"],
        "job_type": "remote",
        "degree_required": "Bachelors",
        "cgpa_required": 7.0
    }
]


def index(request):
    return render(request, 'resume_analysis/index.html')


def extract_education_info(text):
    degree_patterns = {
        "PhD": r"(ph\.?d|doctorate)",
        "Masters": r"(master|m\.sc|m\.tech|mba)",
        "Bachelors": r"(bachelor|b\.sc|b\.tech|b\.com|ba)"
    }
    cgpa_match = re.search(r"\b([0-9]\.?[0-9]{0,2})\s*(cgpa|gpa|percentage|%)\b", text, re.IGNORECASE)
    cgpa = float(cgpa_match.group(1)) if cgpa_match else 0.0

    degree = "Unknown"
    for deg, pattern in degree_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            degree = deg
            break

    return degree, cgpa


def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('resume_file'):
        resume_file = request.FILES['resume_file']
        file_path = os.path.join(settings.MEDIA_ROOT, 'resumes', resume_file.name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save uploaded file
        with open(file_path, 'wb+') as destination:
            for chunk in resume_file.chunks():
                destination.write(chunk)

        resume_text = text_extractor.extract_text(file_path)
        summary = summarizer.summarize_text(resume_text)
        skills = [skill.lower() for skill in skill_matcher.extract_skills(resume_text)]
        degree, cgpa = extract_education_info(resume_text)
        feedback = langchain_flow.generate_feedback(resume_text)

        if not skills:
            feedback += "\nNote: No extractable skills detected from your resume. Consider updating it."

        # Store parsed info in session
        request.session['resume_text'] = resume_text
        request.session['skills'] = skills
        request.session['degree'] = degree
        request.session['cgpa'] = cgpa
        request.session['feedback'] = feedback

        context = {
            'summary': summary,
            'skills': skills,
            'degree': degree,
            'cgpa': cgpa,
            'feedback': feedback,
        }
        return render(request, 'resume_analysis/result.html', context)

    return render(request, 'resume_analysis/index.html')


def match_jobs(resume_text, skills_from_resume, location_pref, skills_pref, experience_pref, job_type_pref, degree, cgpa):
    matched_jobs = []

    for job in ALL_JOBS:
        skill_overlap = len(set(skills_from_resume).intersection({s.lower() for s in job['skills_required']}))
        similarity_score = jd_comparator.compare_with_jd(resume_text, " ".join(job['skills_required']))

        degree_match = (degree.lower() == job['degree_required'].lower()) or (job['degree_required'].lower() == "bachelors")
        cgpa_match = cgpa >= job['cgpa_required']
        experience_match = experience_pref >= job['experience_required']

        location_match = not location_pref or location_pref in job['location'].lower()
        job_type_match = not job_type_pref or job_type_pref == job.get('job_type', '').lower()

        if degree_match and cgpa_match and experience_match and location_match and job_type_match:
            matched_jobs.append({
                "title": job['title'],
                "company": job['company'],
                "description": job['description'],
                "location": job['location'],
                "experience_required": job['experience_required'],
                "skills_required": job['skills_required'],
                "similarity": round(similarity_score * 100, 2),
            })

    return sorted(matched_jobs, key=lambda x: x['similarity'], reverse=True)


def search_jobs(request):
    resume_text = request.session.get('resume_text', None)
    skills_from_resume = request.session.get('skills', [])
    degree = request.session.get('degree', "Unknown")
    cgpa = request.session.get('cgpa', 0.0)

    if not resume_text:
        return render(request, "resume_analysis/search_results.html", {"message": "Please upload your resume first."})

    if request.method == 'POST':
        location_pref = request.POST.get("location", "").lower()
        skills_pref = [s.strip().lower() for s in request.POST.get("skills", "").split(",") if s.strip()]
        experience_pref = int(request.POST.get("experience") or 0)
        job_type_pref = request.POST.get("job_type", "").lower()

        matched_jobs = match_jobs(resume_text, skills_from_resume, location_pref, skills_pref, experience_pref, job_type_pref, degree, cgpa)

        context = {
            "location": location_pref,
            "skills": skills_pref,
            "experience": experience_pref,
            "job_type": job_type_pref,
            "jobs": matched_jobs[:INITIAL_DISPLAY],
            "all_jobs": matched_jobs,
        }

        return render(request, "resume_analysis/search_results.html", context)

    return render(request, "resume_analysis/search_results.html", {"message": "No preferences submitted"})
