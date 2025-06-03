from rest_framework import routers                 # وارد کردن ماژول روترهای DRF جهت استفاده از DefaultRouter
from django.urls import path, include               # وارد کردن توابع path و include برای تعریف و درج URLها
from Advertisements.views import (
    JobAdvertisementViewSet,
    ResumeAdvertisementViewSet,
    ApplicationViewSet
)  # ایمپورت ویوست‌های مربوط به آگهی‌ها از ماژول views اپلیکیشن آگهی‌ها


class JobAdvertisementRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت JobAdvertisementViewSet با prefix خالی و تعیین basename 'JobAdvertisements'
        self.register(r'', JobAdvertisementViewSet, basename='JobAdvertisements')

    def get_urls(self):
        custom_urls = [
            path('', include([
                # مسیر خالی: تعریف متد get (لیست) برای آگهی‌های کارفرما
                path('', JobAdvertisementViewSet.as_view({'get': 'list'})),
                # مسیر شامل پارامتر uuid: برای دریافت (GET) یک آگهی کارفرما و ایجاد (POST) آگهی
                path('<uuid:pk>/', JobAdvertisementViewSet.as_view({'get': 'retrieve', 'post': 'create'})),
                # مسیر شامل یک پارامتر pk از نوع uuid: برای به‌روزرسانی (PUT) یک آگهی کارفرما
                path('<uuid:pk>/', JobAdvertisementViewSet.as_view({'put': 'update'})),
                # مسیر شامل دو پارامتر pk (uuid) و uuid: جهت حذف (DELETE) آگهی کارفرما
                path('<uuid:pk>/', JobAdvertisementViewSet.as_view({'delete': 'destroy'})),
            ])),
        ]
        return custom_urls

# ---------------------------------------------------------------------------
# ResumeAdvertisementRouter: روتر برای مدیریت URLهای مربوط به ResumeAdvertisement (آگهی رزومه کارجو)
# ---------------------------------------------------------------------------
class ResumeAdvertisementRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت ResumeAdvertisementViewSet با prefix خالی و تعیین basename 'ResumeAdvertisements'
        self.register(r'', ResumeAdvertisementViewSet, basename='ResumeAdvertisements')

    def get_urls(self):
        custom_urls = [
            path('', include([
                # مسیر خالی: متدهای get (لیست کردن) و post (ایجاد) برای آگهی‌های رزومه کارجو
                path('', ResumeAdvertisementViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر شامل یک پارامتر pk جهت دریافت (GET) آگهی رزومه کارجو بر اساس pk آگهی
                path('<uuid:pk>/', ResumeAdvertisementViewSet.as_view({'get': 'retrieve'})),
                # مسیر شامل یک پارامتر pk جهت به‌روزرسانی (PUT) آگهی رزومه کارجو
                path('<uuid:pk>/', ResumeAdvertisementViewSet.as_view({'put': 'update'})),
                # مسیر شامل دو پارامتر pk (uuid) و pk جهت حذف (DELETE) آگهی رزومه کارجو
                path('<uuid:pk>/', ResumeAdvertisementViewSet.as_view({'delete': 'destroy'})),
            ])),
        ]
        return custom_urls


class ApplicationRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت ApplicationViewSet با prefix خالی و تعیین basename 'applications'
        self.register(r'', ApplicationViewSet, basename='applications')

    def get_urls(self):
        custom_urls = [
            path('', include([
                # مسیر خالی: متد get (لیست کردن) و post (ایجاد) برای درخواست‌ها
                path('', ApplicationViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر شامل یک پارامتر pk از نوع uuid جهت مدیریت عملیات retrieve، update و delete
                path('<uuid:pk>/', include([
                    path('', ApplicationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
                ])),
            ])),
        ]
        return custom_urls
