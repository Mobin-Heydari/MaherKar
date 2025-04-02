from django.urls import path, include
from Advertisements.routers import ApplicationRouter


app_name = "Advertisements"


applications_router = ApplicationRouter()


urlpatterns = [
    path('applications/', include(applications_router.get_urls())),
]
