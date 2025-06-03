from django.urls import path, include  
# ایمپورت توابع path و include برای تعریف مسیرهای URL و اتصال به روترهای سفارشی

from rest_framework.routers import DefaultRouter  
# ایمپورت کلاس DefaultRouter از DRF برای مدیریت خودکار مسیرهای پایه

from .views import (  
    JobSeekerReportViewSet,
    EmployerReportViewSet
)  
# ایمپورت ویوست‌های مرتبط با گزارش‌های جویندگان کار، کارفرماها، و آگهی‌ها




# ---------------------------------------------------------------------------
# JobSeekerReportRouter: روتر برای مدیریت URLهای مربوط به JobSeekerReport (گزارش جویندگان کار)
# ---------------------------------------------------------------------------
class JobSeekerReportRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت ویوست JobSeekerReportViewSet در روتر با basename 'jobseeker-report'
        self.register(r'', JobSeekerReportViewSet, basename='jobseeker-report')

    def get_urls(self):
        # دریافت URLهای پیش‌فرض از DefaultRouter
        urls = super().get_urls()
        # تعریف URLهای سفارشی برای لیست کردن، دریافت جزئیات، ایجاد، بروزرسانی، و حذف گزارش‌ها
        custom_urls = [
            path('', include([
                # مسیر خالی: لیست کردن (GET) و ایجاد (POST) گزارش‌ها
                path('', JobSeekerReportViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر با شناسه id: دریافت جزئیات (GET)، بروزرسانی (PUT)، و حذف (DELETE) یک گزارش خاص
                path('<int:id>/', JobSeekerReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        # ترکیب URLهای پیش‌فرض با URLهای سفارشی و بازگرداندن مجموعه نهایی URLها
        return urls + custom_urls


# ---------------------------------------------------------------------------
# EmployerReportRouter: روتر برای مدیریت URLهای مربوط به EmployerReport (گزارش کارفرماها)
# ---------------------------------------------------------------------------
class EmployerReportRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت ویوست EmployerReportViewSet در روتر با basename 'employer-report'
        self.register(r'', EmployerReportViewSet, basename='employer-report')

    def get_urls(self):
        # دریافت URLهای پیش‌فرض از DefaultRouter
        urls = super().get_urls()
        # تعریف URLهای سفارشی برای لیست کردن، دریافت جزئیات، ایجاد، بروزرسانی، و حذف گزارش‌ها
        custom_urls = [
            path('', include([
                # مسیر خالی: لیست کردن (GET) و ایجاد (POST) گزارش‌ها
                path('', EmployerReportViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر با شناسه id: دریافت جزئیات (GET)، بروزرسانی (PUT)، و حذف (DELETE) یک گزارش خاص
                path('<int:id>/', EmployerReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        # ترکیب URLهای پیش‌فرض با URLهای سفارشی و بازگرداندن مجموعه نهایی URLها
        return urls + custom_urls