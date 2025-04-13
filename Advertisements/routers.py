from rest_framework import routers                 # وارد کردن ماژول روترهای DRF جهت استفاده از DefaultRouter
from django.urls import path, include               # وارد کردن توابع path و include برای تعریف و درج URLها
from Advertisements.views import (
    AdvertisementViewSet,
    JobAdvertisementViewSet,
    ResumeAdvertisementViewSet,
    ApplicationViewSet
)  # ایمپورت ویوست‌های مربوط به آگهی‌ها از ماژول views اپلیکیشن آگهی‌ها



# ---------------------------------------------------------------------------
# AdvertisementRouter: روتر برای مدیریت URLهای مربوط به Advertisement (آگهی عمومی)
# ---------------------------------------------------------------------------
class AdvertisementRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()  
        # ثبت AdvertisementViewSet با prefix خالی (r'') و تعیین basename 'Advertisements'
        self.register(r'', AdvertisementViewSet, basename='Advertisements')

    def get_urls(self):
        # دریافت URLهای پیش‌فرض تعریف شده توسط DefaultRouter
        urls = super().get_urls()
        # تعریف URLهای سفارشی جهت پوشش عملیات‌های خاص مانند retrieve و update بر مبنای slug
        custom_urls = [
            path('', include([  
                # مسیر خالی: برای عملیات لیست (GET) آگهی‌ها
                path('', AdvertisementViewSet.as_view({'get': 'list'})),
                # مسیر شامل یک پارامتر slug: جهت دریافت و به‌روزرسانی آگهی بر اساس slug
                path('<slug:slug>/', include([
                    # در مسیر slug، متد‌های get (retrieve) و put (update) تعریف شده‌اند
                    path('', AdvertisementViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
                ])),
            ])),
        ]
        # ترکیب URLهای پیش‌فرض و سفارشی و برگرداندن مجموعه نهایی URLها
        return urls + custom_urls

# ---------------------------------------------------------------------------
# JobAdvertisementRouter: روتر برای مدیریت URLهای مربوط به JobAdvertisement (آگهی کارفرما)
# ---------------------------------------------------------------------------
class JobAdvertisementRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت JobAdvertisementViewSet با prefix خالی و تعیین basename 'JobAdvertisements'
        self.register(r'', JobAdvertisementViewSet, basename='JobAdvertisements')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                # مسیر خالی: تعریف متد get (لیست) برای آگهی‌های کارفرما
                path('', JobAdvertisementViewSet.as_view({'get': 'list'})),
                # مسیر شامل پارامتر slug: برای دریافت (GET) یک آگهی کارفرما و ایجاد (POST) آگهی
                path('<slug:slug>/', JobAdvertisementViewSet.as_view({'get': 'retrieve', 'post': 'create'})),
                # مسیر شامل یک پارامتر pk از نوع int: برای به‌روزرسانی (PUT) یک آگهی کارفرما
                path('<int:pk>/', JobAdvertisementViewSet.as_view({'put': 'update'})),
                # مسیر شامل دو پارامتر pk (int) و slug: جهت حذف (DELETE) آگهی کارفرما
                path('<int:pk>/<slug:slug>/', JobAdvertisementViewSet.as_view({'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls

# ---------------------------------------------------------------------------
# ResumeAdvertisementRouter: روتر برای مدیریت URLهای مربوط به ResumeAdvertisement (آگهی رزومه کارجو)
# ---------------------------------------------------------------------------
class ResumeAdvertisementRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت ResumeAdvertisementViewSet با prefix خالی و تعیین basename 'ResumeAdvertisements'
        self.register(r'', ResumeAdvertisementViewSet, basename='ResumeAdvertisements')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                # مسیر خالی: متدهای get (لیست کردن) و post (ایجاد) برای آگهی‌های رزومه کارجو
                path('', ResumeAdvertisementViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر شامل یک پارامتر slug جهت دریافت (GET) آگهی رزومه کارجو بر اساس slug آگهی
                path('<slug:slug>/', ResumeAdvertisementViewSet.as_view({'get': 'retrieve'})),
                # مسیر شامل یک پارامتر pk جهت به‌روزرسانی (PUT) آگهی رزومه کارجو
                path('<int:pk>/', ResumeAdvertisementViewSet.as_view({'put': 'update'})),
                # مسیر شامل دو پارامتر pk (int) و slug جهت حذف (DELETE) آگهی رزومه کارجو
                path('<int:pk>/<slug:slug>/', ResumeAdvertisementViewSet.as_view({'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls

# ---------------------------------------------------------------------------
# ApplicationRouter: روتر برای مدیریت URLهای مربوط به Application (درخواست‌های ارسال شده)
# ---------------------------------------------------------------------------
class ApplicationRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت ApplicationViewSet با prefix خالی و تعیین basename 'applications'
        self.register(r'', ApplicationViewSet, basename='applications')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                # مسیر خالی: متد get (لیست کردن) و post (ایجاد) برای درخواست‌ها
                path('', ApplicationViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر شامل یک پارامتر pk از نوع int جهت مدیریت عملیات retrieve، update و delete
                path('<int:pk>/', include([
                    path('', ApplicationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
                ])),
            ])),
        ]
        return urls + custom_urls
