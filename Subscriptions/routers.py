from django.urls import path, include  
# ایمپورت توابع path و include برای تعریف مسیرهای URL و اتصال به روترهای دیگر

from rest_framework.routers import DefaultRouter  
# وارد کردن کلاس DefaultRouter از DRF برای مدیریت خودکار مسیرهای پایه و عملیات CRUD

from .views import SubscriptionPlanViewSet, AdvertisementSubscriptionViewSet  
# ایمپورت ویوست‌های مربوط به طرح‌های اشتراک و اشتراک‌های آگهی از ماژول views




# ---------------------------------------------------------------------------
# SubscriptionPlanRouter: روتر برای مدیریت URLهای مربوط به SubscriptionPlan (طرح‌های اشتراک)
# ---------------------------------------------------------------------------
class SubscriptionPlanRouter(DefaultRouter):
    def __init__(self):
        super().__init__()  
        # ثبت SubscriptionPlanViewSet در DefaultRouter با prefix خالی و تعیین basename 'subscription-plan'
        self.register(r'', SubscriptionPlanViewSet, basename='subscription-plan')

    def get_urls(self):
        # دریافت URLهای پیش‌فرض از DefaultRouter
        urls = super().get_urls()
        # تعریف URLهای سفارشی برای عملیات‌های مختلف بر اساس شناسه (pk)
        custom_urls = [
            path('', include([
                # مسیر خالی برای دریافت لیست طرح‌ها (GET) و ایجاد طرح جدید (POST)
                path('', SubscriptionPlanViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر با شناسه pk برای دریافت جزئیات طرح (GET)، بروزرسانی (PUT)، و حذف (DELETE)
                path('<int:pk>/', SubscriptionPlanViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        # ترکیب URLهای پیش‌فرض با URLهای سفارشی و بازگردانی مجموعه نهایی URLها
        return urls + custom_urls



# ---------------------------------------------------------------------------
# AdvertisementSubscriptionRouter: روتر برای مدیریت URLهای مربوط به AdvertisementSubscription (اشتراک‌های آگهی)
# ---------------------------------------------------------------------------
class AdvertisementSubscriptionRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت AdvertisementSubscriptionViewSet در DefaultRouter با prefix خالی و تعیین basename 'job-ad-subscription'
        self.register(r'', AdvertisementSubscriptionViewSet, basename='job-ad-subscription')

    def get_urls(self):
        # دریافت URLهای پیش‌فرض از DefaultRouter
        urls = super().get_urls()
        # تعریف URLهای سفارشی برای عملیات‌های مختلف
        custom_urls = [
            path('', include([
                # مسیر خالی برای دریافت لیست اشتراک‌های آگهی (GET)
                path('', AdvertisementSubscriptionViewSet.as_view({'get': 'list'})),
                # مسیر با شناسه pk برای دریافت جزئیات اشتراک آگهی (GET)
                path('<int:pk>/', AdvertisementSubscriptionViewSet.as_view({'get': 'retrieve'})),
            ])),
        ]
        # ترکیب URLهای پیش‌فرض با URLهای سفارشی و بازگردانی مجموعه نهایی URLها
        return urls + custom_urls
