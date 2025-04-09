from django.urls import path  # وارد کردن تابع path جهت تعریف مسیرهای URL
from . import views         # ایمپورت ویوهای تعریف‌شده در فایل views.py به منظور استفاده در URLها



app_name = "Authentication"  # تعریف فضای نام (namespace) برای اپلیکیشن احراز هویت؛ این کار از تداخل URLها در پروژه‌های چند اپ جلوگیری می‌کند



urlpatterns = [
    # مسیر ورود کاربر:
    # وقتی درخواست به /login/ ارسال شود، ویو LoginAPIView اجرا شده و توکن‌های JWT در صورت موفقیت برگردانده می‌شوند.
    path('login/', views.LoginAPIView.as_view(), name="login"),

    # ثبت‌نام با OTP:
    # مسیر register-otp/ برای تولید رمز یکبار مصرف جهت ثبت‌نام کاربر استفاده می‌شود.
    path('register-otp/', views.UserRegisterOtpAPIView.as_view(), name="user_register_otp"),

    # تایید ثبت‌نام با OTP:
    # مسیر register-otp-validate/<str:token>/ برای تایید رمز یکبار مصرف دریافت شده و ایجاد کاربر نهایی بر اساس آن استفاده می‌شود.
    path('register-otp-validate/<str:token>/', views.UserRegisterOtpValidateAPIView.as_view(), name="user_register_otp_validate"),
]
