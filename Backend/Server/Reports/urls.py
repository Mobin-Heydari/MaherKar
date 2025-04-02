from django.urls import path, include
from .routers import (
    JobSeekerReportRouter,
    EmployerReportRouter,
    AdminReportRouter,
    SupportReportRouter,
    JobAdvertisementReportRouter,
)


app_name = "Reports"


# Initialize custom routers
jobseeker_router = JobSeekerReportRouter()
employer_router = EmployerReportRouter()
admin_router = AdminReportRouter()
support_router = SupportReportRouter()
job_advertisement_router = JobAdvertisementReportRouter()


urlpatterns = [
    path('jobseeker/', include(jobseeker_router.get_urls())),
    path('employer/', include(employer_router.get_urls())),
    path('admin/', include(admin_router.get_urls())),
    path('support/', include(support_router.get_urls())),
    path('job-advertisement/', include(job_advertisement_router.get_urls())),
]
