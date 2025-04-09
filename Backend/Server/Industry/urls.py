from django.urls import path, include  # وارد کردن توابع path و include جهت تعریف و افزودن URLها
from .routers import IndustryCategoryRouter, IndustryRouter, SkillRouter  
# ایمپورت روترهای سفارشی مربوط به دسته‌بندی‌های صنعت، صنایع و مهارت‌ها



app_name = "Industry"  # تعریف فضای نام (namespace) برای اپلیکیشن صنعت؛ این کار از تداخل URLها در پروژه‌های چند اپلیکیشنی جلوگیری می‌کند



# ایجاد نمونه‌هایی از روترهای سفارشی:
industry_category_router = IndustryCategoryRouter()  # نمونه‌ای از روتر دسته‌بندی‌های صنعت
industry_router = IndustryRouter()                    # نمونه‌ای از روتر صنایع
skill_router = SkillRouter()                          # نمونه‌ای از روتر مهارت‌ها



# تعریف نهایی الگوهای URL:
urlpatterns = [
    # مسیر 'industry-categories/' تمامی URLهای مربوط به دسته‌بندی‌های صنعت را شامل می‌شود
    path('industry-categories/', include(industry_category_router.urls)),
    # مسیر 'industries/' تمامی URLهای مربوط به صنایع را شامل می‌شود
    path('industries/', include(industry_router.urls)),
    # مسیر 'skills/' تمامی URLهای مربوط به مهارت‌ها را شامل می‌شود
    path('skills/', include(skill_router.urls)),
]
