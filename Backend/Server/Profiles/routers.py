# ایمپورت ماژول‌های مورد نیاز
from rest_framework import routers
from django.urls import path, include

from .views import (
    JobSeekerProfileViewSet,
    EmployerProfileViewSet,
    AdminProfileViewSet,
    SupportProfileViewSet
)



class JobSeekerRouter(routers.DefaultRouter):
    # مقداردهی اولیه روت سفارشی
    def __init__(self):
        super().__init__()
        # ثبت ویوست JobSeekerProfileViewSet در این روت سفارشی
        self.register(r'', JobSeekerProfileViewSet, basename='job-seekers')

    # تعریف یک متد برای دریافت URLهای سفارشی
    def get_urls(self):
        # دریافت URLها از کلاس والد
        urls = super().get_urls()
        # تعریف URLهای سفارشی برای JobSeekerProfileViewSet
        custom_urls = [
            # تعریف یک الگوی URL برای لیست پروفایل‌های جویندگان کار
            path('', include([
                path('', JobSeekerProfileViewSet.as_view({'get': 'list'})),
                # تعریف یک الگوی URL برای جزئیات یک جوینده کار خاص
                path('<str:user__username>/', include([
                    path('', JobSeekerProfileViewSet.as_view({'get': 'retrieve'})),
                ])),
            ])),
        ]
        # بازگشت URLهای سفارشی به علاوه URLهای اولیه
        return urls + custom_urls


class EmployerRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', EmployerProfileViewSet, basename='employers')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', EmployerProfileViewSet.as_view({'get': 'list'})),
                path('<str:user__username>/', include([
                    path('', EmployerProfileViewSet.as_view({'get': 'retrieve'})),
                ])),
            ])),
        ]
        return urls + custom_urls


class AdminRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', AdminProfileViewSet, basename='admins')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', AdminProfileViewSet.as_view({'get': 'list'})),
                path('<str:user__username>/', include([
                    path('', AdminProfileViewSet.as_view({'get': 'retrieve'})),
                ])),
            ])),
        ]
        return urls + custom_urls



class SupportRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', SupportProfileViewSet, basename='supports')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', SupportProfileViewSet.as_view({'get': 'list'})),
                path('<str:user__username>/', include([
                    path('', SupportProfileViewSet.as_view({'get': 'retrieve'})),
                ])),
            ])),
        ]
        return urls + custom_urls
