from django.urls import path, include
from Advertisements.routers import JobAdvertisementRouter, ApplicationRouter, JobseekerResumeAdvertisementRouter


app_name = "Advertisements"


job_advertisements_router = JobAdvertisementRouter()
applications_router = ApplicationRouter()
resume_advertisements_router = JobseekerResumeAdvertisementRouter()


urlpatterns = [
    path('job-advertisements/', include(job_advertisements_router.get_urls())),
    path('applications/', include(applications_router.get_urls())),
    path('resume-advertisements/', include(resume_advertisements_router.get_urls())),
]
