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
        # دریافت URLهای پیش‌فرض از کلاس والد (DefaultRouter)
        urls = super().get_urls()
        # تعریف URLهای سفارشی برای عملیات‌های CRUD دسته‌بندی‌ها
        custom_urls = [
            path('', include([
                # مسیر خالی برای اجرای متد list (GET) و create (POST) دسته‌بندی‌ها
                path('', IndustryCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر شامل پارامتر slug برای دریافت (GET)، به‌روزرسانی (PUT) و حذف (DELETE) یک دسته‌بندی خاص
                path('<slug:slug>/', IndustryCategoryViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'delete': 'destroy'
                })),
            ])),
        ]
        # بازگرداندن ترکیب URLهای پیش‌فرض و سفارشی
        return urls + custom_urls


# ------------------------------------------------------------------
# روتر صنایع (IndustryRouter)
# ------------------------------------------------------------------
class IndustryRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت IndustryViewSet با مسیر پایه خالی و تعیین basename 'industry'
        self.register(r'', IndustryViewSet, basename='industry')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                # مسیر خالی برای فراخوانی متد list (GET) صنایع
                path('', IndustryViewSet.as_view({'get': 'list'})),
                # مسیر برای ایجاد صنعت جدید؛ متد POST به صورت سفارشی تعریف شده و به عنوان پارامتر category_slug دریافت می‌شود
                # (توجه: به نظر می‌رسد "crate" به اشتباه نوشته شده و باید "create" باشد)
                path('crate/<slug:category_slug>', IndustryViewSet.as_view({'post': 'create'})),
                # مسیر شامل پارامتر slug جهت دریافت (GET)، به‌روزرسانی (PUT) و حذف (DELETE) یک صنعت خاص
                path('<slug:slug>/', IndustryViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'delete': 'destroy'
                })),
            ])),
        ]
        return urls + custom_urls
    


# ------------------------------------------------------------------
# روتر مهارت‌ها (SkillRouter)
# ------------------------------------------------------------------
class SkillRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت SkillViewSet با مسیر پایه خالی و تعیین basename 'skill'
        self.register(r'', SkillViewSet, basename='skill')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                # مسیر خالی برای دسترسی به متد list (GET) مهارت‌ها
                path('', SkillViewSet.as_view({'get': 'list'})),
                # مسیر برای ایجاد مهارت جدید؛ انتظار می‌رود در URL industry_slug ارسال شود تا مهارت به صنعت مربوطه متصل گردد
                # (توجه: در اینجا هم "crate" به اشتباه نوشته شده و احتمالاً باید "create" باشد، همچنین باید از SkillViewSet استفاده شود نه IndustryViewSet)
                path('crate/<slug:industry_slug>', IndustryViewSet.as_view({'post': 'create'})),
                # مسیر شامل پارامتر name (به عنوان رشته) جهت دریافت (GET)، به‌روزرسانی (PUT) و حذف (DELETE) یک مهارت مشخص
                path('<str:name>/', SkillViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'delete': 'destroy'
                })),
            ])),
        ]
        return urls + custom_urls
