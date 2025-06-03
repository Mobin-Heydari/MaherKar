from django.urls import path, include  # ایمپورت توابع path و include برای تعریف و درج URLها
from .routers import (              # ایمپورت روترهای سفارشی مربوط به مدل‌های رزومه
    JobSeekerResumeRouter,
    ExperienceRouter,
    EducationRouter,
    JobSeekerSkillRouter,
)


app_name = "Resumes"  # تعریف namespace برای اپلیکیشن رزومه‌ها جهت جلوگیری از تداخل نام‌های URL در پروژه


# ایجاد نمونه‌هایی از روترهای سفارشی:
job_seeker_resumes_router = JobSeekerResumeRouter()  # ایجاد نمونه‌ای از روتر مربوط به رزومه‌های جوینده کار
experiences_router = ExperienceRouter()              # ایجاد نمونه‌ای از روتر مربوط به تجربیات کاری
educations_router = EducationRouter()                # ایجاد نمونه‌ای از روتر مربوط به تحصیلات
skills_router = JobSeekerSkillRouter()               # ایجاد نمونه‌ای از روتر مربوط به مهارت‌های رزومه جوینده کار



# تعریف الگوهای URL کلی اپ رزومه‌ها:
urlpatterns = [
    # مسیر 'resumes/' شامل URLهای مربوط به رزومه‌های جوینده کار می‌باشد
    path('resumes/', include(job_seeker_resumes_router.get_urls())),
    # مسیر 'experiences/' شامل URLهای مربوط به تجربیات کاری می‌باشد
    path('experiences/', include(experiences_router.get_urls())),
    # مسیر 'educations/' شامل URLهای مربوط به تحصیلات می‌باشد
    path('educations/', include(educations_router.get_urls())),
    # مسیر 'skills/' شامل URLهای مربوط به مهارت‌های رزومه می‌باشد
    path('skills/', include(skills_router.get_urls())),
]
