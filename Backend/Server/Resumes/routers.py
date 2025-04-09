from rest_framework import routers  # وارد کردن مدول روترهای DRF
from django.urls import path, include  # وارد کردن توابع path و include جهت تعریف URL
from .views import (
    JobSeekerResumeViewSet,
    ExperienceViewSet,
    EducationViewSet,
    JobSeekerSkillViewSet,
)



# ---------------------------------------------------------
# روتر رزومه‌های جوینده کار (JobSeekerResumeRouter)
# ---------------------------------------------------------
class JobSeekerResumeRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت ویوست JobSeekerResumeViewSet با basename 'job-seeker-resumes'
        self.register(r'', JobSeekerResumeViewSet, basename='job-seeker-resumes')

    def get_urls(self):
        # دریافت URLهای پیش‌فرض از کلاس والد
        urls = super().get_urls()
        # تعریف URLهای سفارشی جهت پوشش عملیات‌های list, create, retrieve, update, destroy
        custom_urls = [
            path('', include([
                # مسیر خالی برای دسترسی به متد‌های list و create
                path('', JobSeekerResumeViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر با پارامتر pk برای دسترسی به عملیات retrieve, update و destroy
                path('<int:pk>/', include([
                    path('', JobSeekerResumeViewSet.as_view({
                        'get': 'retrieve', 
                        'put': 'update', 
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        # ترکیب URLهای پیش‌فرض و سفارشی و بازگردانی کل مجموعه
        return urls + custom_urls


# ---------------------------------------------------------
# روتر تجربیات کاری (ExperienceRouter)
# ---------------------------------------------------------
class ExperienceRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت ویوست ExperienceViewSet با basename 'experiences'
        self.register(r'', ExperienceViewSet, basename='experiences')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                # مسیر خالی برای عملیات لیست و ایجاد (GET و POST) تجربیات کاری
                path('', ExperienceViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر با پارامتر pk جهت عملیات دریافت، به‌روزرسانی و حذف تجربه کاری
                path('<int:pk>/', include([
                    path('', ExperienceViewSet.as_view({
                        'get': 'retrieve', 
                        'put': 'update', 
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return urls + custom_urls


# ---------------------------------------------------------
# روتر تحصیلات (EducationRouter)
# ---------------------------------------------------------
class EducationRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت ویوست EducationViewSet با basename 'educations'
        self.register(r'', EducationViewSet, basename='educations')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                # مسیر خالی جهت دسترسی به عملیات لیست و ایجاد تحصیلات (GET و POST)
                path('', EducationViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر با پارامتر pk برای دسترسی به عملیات دریافت، به‌روزرسانی و حذف تحصیلات
                path('<int:pk>/', include([
                    path('', EducationViewSet.as_view({
                        'get': 'retrieve', 
                        'put': 'update', 
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return urls + custom_urls


# ---------------------------------------------------------
# روتر مهارت‌های رزومه جوینده کار (JobSeekerSkillRouter)
# ---------------------------------------------------------
class JobSeekerSkillRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت ویوست JobSeekerSkillViewSet با basename 'skills'
        self.register(r'', JobSeekerSkillViewSet, basename='skills')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                # مسیر خالی جهت دسترسی به عملیات لیست و ایجاد مهارت‌ها (GET و POST)
                path('', JobSeekerSkillViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر با پارامتر pk برای دریافت، به‌روزرسانی و حذف یک مهارت
                path('<int:pk>/', include([
                    path('', JobSeekerSkillViewSet.as_view({
                        'get': 'retrieve', 
                        'put': 'update', 
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return urls + custom_urls
