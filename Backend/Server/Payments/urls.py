from django.urls import path  
# ایمپورت تابع path جهت تعریف مسیرهای URL

from . import views  
# ایمپورت ویوهای تعریف‌شده در فایل views اپ پرداخت



app_name = "Payments"  
# تعریف فضای نام (namespace) برای اپ پرداخت؛ این نام به جلوگیری از تداخل URLها کمک می‌کند و اجازه می‌دهد URLها با نام مشخص فراخوانی شوند (مانند Payments:zarinpal-pay).



urlpatterns = [
    # مسیر 'zarinpal-pay/<str:order_id>/'
    # این مسیر برای ارسال درخواست پرداخت به درگاه Zarinpal استفاده می‌شود.
    # <str:order_id> یک پارامتر داینامیک است که شناسه سفارش را دریافت می‌کند.
    # views.SendPaymentRequest.as_view() ویو مرتبط را فراخوانی می‌کند.
    path('zarinpal-pay/<str:order_id>/', views.SendPaymentRequest.as_view()),

    # مسیر 'zarinpal-verify/'
    # این مسیر برای تایید تراکنش پرداخت استفاده می‌شود.
    # این مسیر برای مدیریت فرآیند تایید پرداخت و به‌روزرسانی وضعیت سفارشات طراحی شده است.
    path('zarinpal-verify/', views.VerifyPaymentRequest.as_view())
]
