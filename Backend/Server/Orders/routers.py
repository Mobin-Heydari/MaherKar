from django.urls import path, include  
# ایمپورت توابع path و include برای تعریف مسیرهای URL و اتصال به روترهای دیگر

from rest_framework.routers import DefaultRouter  
# وارد کردن کلاس DefaultRouter از DRF برای مدیریت خودکار مسیرهای پایه و عملیات CRUD

from .views import SubscriptionOrderViewSet  
# ایمپورت SubscriptionOrderViewSet از فایل views جهت استفاده در روتر


# ---------------------------------------------------------------------------
# SubscriptionOrderRouter: روتر برای مدیریت URLهای مربوط به SubscriptionOrder (سفارش اشتراک)
# ---------------------------------------------------------------------------
class SubscriptionOrderRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت SubscriptionOrderViewSet در DefaultRouter با prefix خالی و تعیین basename 'SubscriptionOrder'
        self.register(r'', SubscriptionOrderViewSet, basename='SubscriptionOrder')

    def get_urls(self):
        # دریافت URLهای پیش‌فرض از DefaultRouter
        urls = super().get_urls()
        # تعریف URLهای سفارشی جهت مدیریت عملیات‌های لیست کردن، دریافت جزئیات، و ایجاد سفارش
        custom_urls = [
            path('', include([
                # مسیر خالی برای دریافت لیست سفارشات (GET)
                path('', SubscriptionOrderViewSet.as_view({'get': 'list'})),
                # مسیر شامل شناسه سفارش (order_id) برای دریافت جزئیات سفارش (GET)
                path('<str:order_id>/', SubscriptionOrderViewSet.as_view({'get': 'retreive'})),
                # مسیر شامل شناسه طرح، شناسه اشتراک، و slug آگهی برای ایجاد سفارش جدید (POST)
                path('<int:plan_id>/<int:subscription_id>/<slug:ad_slug>/', SubscriptionOrderViewSet.as_view({'post': 'create'})),
            ])),
        ]
        # ترکیب URLهای پیش‌فرض با URLهای سفارشی و بازگرداندن مجموعه نهایی URLها
        return urls + custom_urls
