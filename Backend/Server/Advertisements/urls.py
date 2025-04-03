from django.urls import path, include
from Advertisements.routers import AdvertisementRouter, ApplicationRouter


app_name = "Advertisements"

ad_router = AdvertisementRouter()
applications_router = ApplicationRouter()


urlpatterns = [
    path('advertisments/', include(ad_router.get_urls())),
    path('applications/', include(applications_router.get_urls()))
]
