from django.urls import path, include
from .routers import CompanyRouter



app_name = "Companies"


router = CompanyRouter()


urlpatterns = [
    path('', include(router.urls)),
]