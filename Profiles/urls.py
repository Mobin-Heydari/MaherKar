from django.urls import path, include  # ایمپورت توابع path و include برای تعریف الگوهای URL
from .routers import JobSeekerRouter, EmployerRouter, AdminRouter, SupportRouter  # ایمپورت روترهای سفارشی مربوط به پروفایل‌های مختلف
from . import views


app_name = "Profiles"  # تعریف namespace برای این اپلیکیشن جهت جداسازی URLها در پروژه



# ایجاد نمونه‌هایی از روترهای سفارشی برای پوشش درخواست‌های مربوط به هر مدل پروفایل:
job_seeker_router = JobSeekerRouter()   # ایجاد نمونه‌ای از JobSeekerRouter جهت مدیریت URLهای مربوط به پروفایل‌های جویندگان کار
employer_router = EmployerRouter()        # ایجاد نمونه‌ای از EmployerRouter جهت مدیریت URLهای مربوط به پروفایل‌های کارفرما
admin_router = AdminRouter()              # ایجاد نمونه‌ای از AdminRouter جهت مدیریت URLهای مربوط به پروفایل‌های مدیر
support_router = SupportRouter()          # ایجاد نمونه‌ای از SupportRouter جهت مدیریت URLهای مربوط به پروفایل‌های پشتیبان



# تعریف نهایی URLها:
urlpatterns = [
    # مسیر 'job-seekers/' تمامی درخواست‌های مربوط به جویندگان کار را مدیریت می‌کند
    path('job-seekers/', include(job_seeker_router.get_urls())),
    # مسیر 'employers/' تمامی درخواست‌های مربوط به کارفرمایان را مدیریت می‌کند
    path('employers/', include(employer_router.get_urls())),
    # مسیر 'admins/' تمامی درخواست‌های مربوط به مدیران را مدیریت می‌کند
    path('admins/', include(admin_router.get_urls())),
    # مسیر 'supports/' تمامی درخواست‌های مربوط به پشتیبان‌ها (Support) را مدیریت می‌کند
    path('supports/', include(support_router.get_urls())),
    # مسیر 'me/' برای دریافت اطلاعات پروفایل همه ی انواع کاربر هاست.
    path('me/', views.UserProfileAPIView.as_view(), name="me")
]
