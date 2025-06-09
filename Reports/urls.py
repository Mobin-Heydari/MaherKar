from django.urls import path, include
from .routers import (
    ReportCategoryRouter,
    EmployerReportRouter,
    JobSeekerReportRouter,
    AdvertisementReportRouter,
)




app_name = "Reports"


report_category_router = ReportCategoryRouter()
jobseeker_router = JobSeekerReportRouter()
employer_router = EmployerReportRouter()
job_advertisement_router = AdvertisementReportRouter()


urlpatterns = [
    path('categories/', include(report_category_router.get_urls())),
    path('jobseeker-reports/', include(jobseeker_router.get_urls())),
    path('employer-reports/', include(employer_router.get_urls())),
    path('advertisement-reports/', include(job_advertisement_router.get_urls())),
]
