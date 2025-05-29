from django.urls import path, include       # وارد کردن توابع path و include برای تعریف و درج URLها
from rest_framework.routers import DefaultRouter  # وارد کردن کلاس DefaultRouter برای ساخت روترهای سفارشی

from .views import IndustryViewSet, IndustryCategoryViewSet, SkillViewSet
# ایمپورت ویوست‌های مربوط به صنایع، دسته‌بندی‌های صنایع و مهارت‌ها



# ------------------------------------------------------------------
# روتر دسته‌بندی‌های صنعت (IndustryCategoryRouter)
# ------------------------------------------------------------------
class IndustryCategoryRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت IndustryCategoryViewSet با مسیر پایه خالی و تعیین basename 'industry-category'
        self.register(r'', IndustryCategoryViewSet, basename='industry-category')

    def get_urls(self):
        # تعریف URLهای سفارشی برای عملیات‌های CRUD دسته‌بندی‌ها
        custom_urls = [
            path('', include([
                # مسیر خالی برای اجرای متد list (GET) و create (POST) دسته‌بندی‌ها
                path('', IndustryCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر شامل پارامتر int برای دریافت (GET)، به‌روزرسانی (PUT) و حذف (DELETE) یک دسته‌بندی خاص
                path('<int:pk>/', IndustryCategoryViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'delete': 'destroy'
                })),
            ])),
        ]
        # بازگرداندن ترکیب URLهای پیش‌فرض و سفارشی
        return custom_urls


# ------------------------------------------------------------------
# روتر صنایع (IndustryRouter)
# ------------------------------------------------------------------
class IndustryRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت IndustryViewSet با مسیر پایه خالی و تعیین basename 'industry'
        self.register(r'', IndustryViewSet, basename='industry')

    def get_urls(self):
        custom_urls = [
            path('', include([
                # مسیر خالی برای فراخوانی متد list (GET) صنایع
                path('', IndustryViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر شامل پارامتر int جهت دریافت (GET)، به‌روزرسانی (PUT) و حذف (DELETE) یک صنعت خاص
                path('<int:pk>/', IndustryViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'delete': 'destroy'
                })),
            ])),
        ]
        return custom_urls
    


# ------------------------------------------------------------------
# روتر مهارت‌ها (SkillRouter)
# ------------------------------------------------------------------
class SkillRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت SkillViewSet با مسیر پایه خالی و تعیین basename 'skill'
        self.register(r'', SkillViewSet, basename='skill')

    def get_urls(self):
        custom_urls = [
            path('', include([
                # مسیر خالی برای دسترسی به متد list (GET) مهارت‌ها
                path('', SkillViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر شامل پارامتر pk (به عنوان رشته) جهت دریافت (GET)، به‌روزرسانی (PUT) و حذف (DELETE) یک مهارت مشخص
                path('<int:pk>/', SkillViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'delete': 'destroy'
                })),
            ])),
        ]
        return custom_urls
