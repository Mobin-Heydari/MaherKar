from django.urls import path, include  
# ایمپورت توابع path و include برای تعریف مسیرهای URL و اتصال به روترهای سفارشی

from .routers import (
    JobSeekerReportRouter,
    EmployerReportRouter,
)  
# ایمپورت روترهای سفارشی مربوط به گزارش‌های جویندگان کار، کارفرماها و آگهی‌ها



app_name = "Reports"  
# تعریف فضای نام (namespace) برای اپ گزارش‌ها؛ این نامگذاری از تداخل URLها با اپلیکیشن‌های دیگر جلوگیری می‌کند و امکان فراخوانی دقیق مسیرها را فراهم می‌آورد.


# ایجاد نمونه‌هایی از روترهای سفارشی
jobseeker_router = JobSeekerReportRouter()
employer_router = EmployerReportRouter()


# تعریف الگوهای URL
urlpatterns = [
    # مسیر 'jobseeker/' برای مدیریت گزارش‌های جویندگان کار؛
    # از طریق jobseeker_router.get_urls() تمامی مسیرهای ثبت‌شده در روتر مربوطه درج می‌شود.
    path('jobseeker/', include(jobseeker_router.get_urls())),

    # مسیر 'employer/' برای مدیریت گزارش‌های کارفرماها؛
    # از طریق employer_router.get_urls() تمامی مسیرهای ثبت‌شده در روتر مربوطه درج می‌شود.
    path('employer/', include(employer_router.get_urls())),
]
