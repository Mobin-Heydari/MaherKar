from django.urls import path, include  
# ایمپورت توابع path و include برای تعریف الگوهای URL

from Advertisements.routers import AdvertisementRouter, JobAdvertisementRouter, ResumeAdvertisementRouter, ApplicationRouter  
# ایمپورت روترهای سفارشی مربوط به اپ آگهی‌ها از ماژول routers



app_name = "Advertisements"  # تعریف فضای نام (namespace) برای اپ آگهی‌ها تا هنگام ارجاع به URLها از نام منحصربه‌فرد استفاده شود



# ایجاد نمونه‌هایی از روترها برای بخش‌های مختلف اپ آگهی‌ها
ad_router = AdvertisementRouter()
job_ad_router = JobAdvertisementRouter()
resume_ad_router = ResumeAdvertisementRouter()
applications_router = ApplicationRouter()


urlpatterns = [
    # مسیر 'advertisments/' تمامی URLهای مربوط به آگهی‌های عمومی را شامل می‌شود؛
    # به کمک ad_router.get_urls()، URLهای تعریف‌شده توسط AdvertisementRouter به این مسیر اضافه می‌شوند.
    path('advertisments/', include(ad_router.get_urls())),
    
    # مسیر 'job/' شامل URLهای مربوط به آگهی‌های کارفرما می‌باشد؛
    # در اینجا job_ad_router.get_urls() URLهای ثبت‌شده برای بخش کارفرما را اضافه می‌کند.
    path('job/', include(job_ad_router.get_urls())),
    
    # مسیر 'resume/' شامل URLهای مربوط به آگهی‌های رزومه کارجو است؛
    # به کمک resume_ad_router.get_urls()، URLهای تعریف‌شده جهت آگهی‌های رزومه اضافه می‌شود.
    path('resume/', include(resume_ad_router.get_urls())),
    
    # مسیر 'applications/' شامل URLهای مربوط به درخواست‌ها (Application) می‌باشد؛
    # از طریق applications_router.get_urls()، URLهای مربوط به عملیات CRUD بر روی درخواست‌ها مدیریت می‌شود.
    path('applications/', include(applications_router.get_urls()))
]
