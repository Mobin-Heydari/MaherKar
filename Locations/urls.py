# urls.py
from django.urls import path, include  # ایمپورت توابع path و include برای تعریف مسیرهای URL
from .routers import ProvinceRouter, CityRouter  # وارد کردن روترهای سفارشی مربوط به استان‌ها و شهرها



app_name = "Locations"  # تعریف فضای نام (namespace) برای اپلیکیشن Locations؛ این کار از تداخل نام‌های URL در پروژه‌های چند اپ جلوگیری می‌کند



# ایجاد نمونه‌هایی از روترهای سفارشی:
province_router = ProvinceRouter()  # نمونه‌ای از روتر استان‌ها
city_router = CityRouter()          # نمونه‌ای از روتر شهرها



# تعریف نهایی URLها:
urlpatterns = [
    # مسیر 'provinces/' شامل تمامی URLهایی است که توسط ProvinceRouter فراهم آمده است
    path('provinces/', include(province_router.urls)),
    # مسیر 'cities/' شامل تمامی URLهایی است که توسط CityRouter فراهم شده است
    path('cities/', include(city_router.urls)),
]
