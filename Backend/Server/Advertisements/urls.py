from django.urls import path, include
from Advertisements.routers import JobAdvertisementRouter, ApplicationRouter


app_name = "Advertisements"


job_advertisements_router = JobAdvertisementRouter()
applications_router = ApplicationRouter()


urlpatterns = [
    path('job-advertisements/', include(job_advertisements_router.get_urls())),
    path('applications/', include(applications_router.get_urls())),
]
