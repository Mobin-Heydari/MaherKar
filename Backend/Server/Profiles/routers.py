# ایمپورت ماژول‌های مورد نیاز:
from rest_framework import routers  # وارد کردن روترهای پیش‌فرض Django REST Framework
from django.urls import path, include  # وارد کردن توابع path و include برای تعریف الگوهای URL

# ایمپورت ویوست‌های مربوط به پروفایل‌های مختلف (جوینده کار، کارفرما، مدیر و پشتیبان)
from .views import (
    JobSeekerProfileViewSet,
    EmployerProfileViewSet,
    AdminProfileViewSet,
    SupportProfileViewSet
)


# -------------------------------
# تعریف روتر سفارشی برای پروفایل‌های جویندگان کار
# -------------------------------
class JobSeekerRouter(routers.DefaultRouter):
    # مقداردهی اولیه روتر سفارشی برای جویندگان کار
    def __init__(self):
        super().__init__()  # فراخوانی سازنده‌ی کلاس والد DefaultRouter
        # ثبت ویوست JobSeekerProfileViewSet در این روتر با basename 'job-seekers'
        self.register(r'', JobSeekerProfileViewSet, basename='job-seekers')

    # متد get_urls جهت تعریف URLهای سفارشی به همراه URLهای پیش‌فرض
    def get_urls(self):
        urls = super().get_urls()  # دریافت URLهای پیش‌فرض تعریف شده توسط DefaultRouter
        # تعریف URLهای سفارشی برای عملیات لیست، جزئیات و به‌روزرسانی پروفایل‌های جویندگان کار
        custom_urls = [
            path('', include([
                # مسیر خالی جهت فراخوانی متد list در JobSeekerProfileViewSet (دریافت لیست پروفایل‌ها)
                path('', JobSeekerProfileViewSet.as_view({'get': 'list'})),
                # مسیر دارای پارامتر pk جهت دریافت جزئیات یک پروفایل خاص
                path('<int:pk>/', JobSeekerProfileViewSet.as_view({'get': 'retrieve'})),
                path('update/<int:pk>/', JobSeekerProfileViewSet.as_view({'put': 'update'})),
            ])),
        ]
        # ترکیب URLهای پیش‌فرض با URLهای سفارشی و بازگردانی کل مجموعه
        return urls + custom_urls


# -------------------------------
# تعریف روتر سفارشی برای پروفایل‌های کارفرمایان
# -------------------------------
class EmployerRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت ویوست EmployerProfileViewSet در این روتر با basename 'employers'
        self.register(r'', EmployerProfileViewSet, basename='employers')

    def get_urls(self):
        urls = super().get_urls()  # دریافت URLهای پیش‌فرض از والد
        # تعریف URLهای سفارشی برای عملیات لیست و جزئیات/به‌روزرسانی پروفایل‌های کارفرما
        custom_urls = [
            path('', include([
                # مسیر خالی جهت فراخوانی متد list (دریافت لیست پروفایل‌های کارفرما)
                path('', EmployerProfileViewSet.as_view({'get': 'list'})),
                # مسیر دارای پارامتر pk جهت دریافت جزئیات یا به‌روزرسانی یک پروفایل کارفرما
                path('<int:pk>/', EmployerProfileViewSet.as_view({'get': 'retrieve'})),
                path('update/<int:pk>/', EmployerProfileViewSet.as_view({'put': 'update'})),
            ])),
        ]
        # ترکیب URLهای پیش‌فرض با URLهای سفارشی و بازگردانی کل مجموعه
        return urls + custom_urls


# -------------------------------
# تعریف روتر سفارشی برای پروفایل‌های مدیر
# -------------------------------
class AdminRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت ویوست AdminProfileViewSet در این روتر با basename 'admins'
        self.register(r'', AdminProfileViewSet, basename='admins')

    def get_urls(self):
        urls = super().get_urls()  # دریافت URLهای پیش‌فرض
        # تعریف URLهای سفارشی جهت دریافت لیست و جزئیات/به‌روزرسانی پروفایل‌های مدیر
        custom_urls = [
            path('', include([
                # مسیر خالی جهت فراخوانی متد list برای دریافت لیست پروفایل‌های مدیر
                path('', AdminProfileViewSet.as_view({'get': 'list'})),
                # مسیر دارای پارامتر pk جهت دریافت اطلاعات یک پروفایل مدیر
                path('<int:pk>/', AdminProfileViewSet.as_view({'get': 'retrieve'})),
                path('update/<int:pk>/', AdminProfileViewSet.as_view({'put': 'update'})),
            ])),
        ]
        # برگشت تمام URLهای به صورت ترکیبی
        return urls + custom_urls


# -------------------------------
# تعریف روتر سفارشی برای پروفایل‌های پشتیبان
# -------------------------------
class SupportRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت ویوست SupportProfileViewSet در این روتر با basename 'supports'
        self.register(r'', SupportProfileViewSet, basename='supports')

    def get_urls(self):
        urls = super().get_urls()  # دریافت URLهای پیش‌فرض از کلاس والد
        # تعریف URLهای سفارشی برای فرآیندهای لیست، دریافت جزئیات و به‌روزرسانی پروفایل‌های پشتیبان
        custom_urls = [
            path('', include([
                # مسیر خالی جهت فراخوانی متد list (دریافت لیست پروفایل‌های پشتیبان)
                path('', SupportProfileViewSet.as_view({'get': 'list'})),
                # مسیر دارای پارامتر pk برای دریافت یا به‌روزرسانی یک پروفایل پشتیبان خاص
                path('<int:pk>/', SupportProfileViewSet.as_view({'get': 'retrieve'})),
                path('update/<int:pk>/', SupportProfileViewSet.as_view({'put': 'update'})),
            ])),
        ]
        # ترکیب URLهای پیش‌فرض با سفارشی و بازگردانی کل مجموعه URL
        return urls + custom_urls
