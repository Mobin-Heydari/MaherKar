from django.urls import path, include
from Advertisements.routers import AdvertisementRouter, JobAdvertisementRouter, ResumeAdvertisementRouter, ApplicationRouter


app_name = "Advertisements"

ad_router = AdvertisementRouter()
job_ad_router = AdvertisementRouter()
resume_ad_router = AdvertisementRouter()
applications_router = ApplicationRouter()


urlpatterns = [
    path('advertisments/', include(ad_router.get_urls())),
    path('job/', include(job_ad_router.get_urls())),
    path('resume/', include(resume_ad_router.get_urls())),
    path('applications/', include(applications_router.get_urls()))
]
