from django.urls import path, include
from .routers import IndustryCategoryRouter, IndustryRouter, SkillRouter  # Import your custom routers



app_name = "Industry"


industry_category_router = IndustryCategoryRouter()
industry_router = IndustryRouter()
skill_router = SkillRouter()



urlpatterns = [
    path('industry-categories/', include(industry_category_router.urls)),
    path('industries/', include(industry_router.urls)),
    path('skills/', include(skill_router.urls)),
]
