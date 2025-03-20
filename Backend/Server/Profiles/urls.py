from django.urls import path, include
from .routers import JobSeekerRouter, EmployerRouter, AdminRouter, SupportRouter



app_name = "Profiles"


# ایجاد نمونه‌هایی از روترهای سفارشی
job_seeker_router = JobSeekerRouter()
employer_router = EmployerRouter()
admin_router = AdminRouter()
support_router = SupportRouter()



# تعریف آدرس‌های URL
urlpatterns = [
    path('job-seekers/', include(job_seeker_router.get_urls())),
    path('employers/', include(employer_router.get_urls())),
    path('admins/', include(admin_router.get_urls())),
    path('supports/', include(support_router.get_urls())),
]
