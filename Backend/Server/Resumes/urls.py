from django.urls import path, include
from .routers import (
    JobSeekerResumeRouter,
    ExperienceRouter,
    EducationRouter,
    JobSeekerSkillRouter,
)

app_name = "Resumes"

# Instantiate the routers
job_seeker_resumes_router = JobSeekerResumeRouter()
experiences_router = ExperienceRouter()
educations_router = EducationRouter()
skills_router = JobSeekerSkillRouter()

# URL patterns
urlpatterns = [
    path('resumes/', include(job_seeker_resumes_router.get_urls())),
    path('experiences/', include(experiences_router.get_urls())),
    path('educations/', include(educations_router.get_urls())),
    path('skills/', include(skills_router.get_urls())),
]
