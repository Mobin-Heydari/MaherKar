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
        # تعریف URLهای سفارشی جهت مدیریت عملیات‌های لیست کردن، دریافت جزئیات، و ایجاد سفارش
        custom_urls = [
            path('', include([
                # مسیر خالی برای دریافت لیست سفارشات (GET)
                path('', SubscriptionOrderViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر شامل شناسه سفارش (order_id) برای دریافت جزئیات سفارش (GET)
                path('<uuid:order_id>/', SubscriptionOrderViewSet.as_view({'get': 'retreive'})),
            ])),
        ]
        # ترکیب URLهای پیش‌فرض با URLهای سفارشی و بازگرداندن مجموعه نهایی URLها
        return custom_urls