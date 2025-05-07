from django.urls import path  # وارد کردن تابع path جهت تعریف مسیرهای URL در اپلیکیشن
from . import views         # وارد کردن ویوهای تعریف‌شده در فایل views.py جهت استفاده در URLها




app_name = "Authentication"  # تعریف فضای نام (namespace) برای اپلیکیشن احراز هویت؛ این کار از تداخل URLها در پروژه‌های چند اپ جلوگیری می‌کند


urlpatterns = [
    # مسیر ورود کاربر:
    # وقتی درخواست به آدرس /login/ ارسال شود، ویو LoginAPIView اجرا شده و در صورت موفقیت، توکن‌های JWT به کاربر بازگردانده می‌شود.
    path('login/', views.LoginAPIView.as_view(), name="login"),

    # مسیر ثبت‌نام با OTP:
    # درخواست‌های ارسال شده به /register-otp/ به ویو UserRegisterOtpAPIView ارسال می‌شوند تا رمز یکبار مصرف جهت ثبت‌نام کاربر تولید شود.
    path('register-otp/', views.UserRegisterOtpAPIView.as_view(), name="user_register_otp"),

    # مسیر تایید ثبت‌نام با OTP:
    # درخواست‌هایی که شامل توکن OTP در URL هستند (/register-otp-validate/<str:token>/) به ویو UserRegisterOtpValidateAPIView هدایت می‌شوند.
    # این ویو مسئول تأیید رمز یکبار مصرف دریافت‌شده و نهایی‌سازی ثبت‌نام کاربر است.
    path('register-otp-validate/<str:token>/', views.UserRegisterOtpValidateAPIView.as_view(), name="user_register_otp_validate"),

    # مسیر تولید OTP جهت ورود کاربر:
    # درخواست‌های ارسال شده به /login-otp/ به ویو UserLoginOneTimePasswordAPIView ارسال می‌شوند تا رمز یکبار مصرف ورود تولید و پیامک شود.
    path('login-otp/', views.UserLoginOneTimePasswordAPIView.as_view()),

    # مسیر تایید OTP جهت ورود کاربر:
    # درخواست‌هایی که شامل توکن OTP در URL هستند (/login-validate-otp/<str:token>/) به ویو UserLoginValidateOneTimePasswordAPIView ارسال می‌شوند.
    # این ویو صحت کد OTP وارد شده توسط کاربر را بررسی کرده و در صورت صحیح بودن، توکن‌های JWT را بازمی‌گرداند.
    path('login-validate-otp/<str:token>/', views.UserLoginValidateOneTimePasswordAPIView.as_view())
]
