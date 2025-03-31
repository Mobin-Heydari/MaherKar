from django.urls import path, include
from .routers import CompanyRouter


app_name = "Companies"


# Create an instance of your custom router
router = CompanyRouter()




# Define URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
