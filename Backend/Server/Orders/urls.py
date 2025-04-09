from django.urls import path, include  
# ایمپورت توابع path و include برای تعریف مسیرهای URL و اتصال به روترهای دیگر

from .routers import SubscriptionOrderRouter  
# ایمپورت روتر سفارشی مربوط به SubscriptionOrder از فایل routers


app_name = "Orders"


# ایجاد نمونه‌ای از روتر سفارش اشتراک
sub_orders = SubscriptionOrderRouter()  
# نمونه‌ای از SubscriptionOrderRouter جهت مدیریت مسیرهای مرتبط با سفارشات اشتراک


# تعریف الگوهای URL
urlpatterns = [
    # مسیر 'subscription-orders/' شامل تمامی URLهای مربوط به سفارشات اشتراک است؛
    # از طریق sub_orders.urls، URLهای تعریف‌شده توسط SubscriptionOrderRouter درج می‌شوند.
    path('subscription-orders/', include(sub_orders.urls)),
]
