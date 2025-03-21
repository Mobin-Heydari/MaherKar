from django.db import models
from django.utils import timezone


# کلاس مدل رمز یکبار مصرف
class OneTimePassword(models.Model):
    # Enum برای وضعیت رمز یکبار مصرف با استفاده از TextChoices Django
    class OtpStatus(models.TextChoices):
        EXPIRED = 'EXP', 'منقضی شده'  # نشان‌دهنده رمز یکبار مصرف منقضی شده
        ACTIVE = 'ACT', 'فعال'         # نشان‌دهنده رمز یکبار مصرف فعال
    
    # فیلد برای ذخیره وضعیت رمز یکبار مصرف (فعال یا منقضی شده)
    status = models.CharField(
        verbose_name="وضعیت",
        max_length=3,
        choices=OtpStatus.choices,
        default=OtpStatus.ACTIVE  # وضعیت پیش‌فرض فعال است
    )
    
    # فیلد برای ذخیره شماره تلفن کاربر
    Phone = models.CharField(
        verbose_name="شماره تلفن",
        max_length=11
    )
    
    # فیلد منحصر به فرد برای ذخیره توکن رمز یکبار مصرف
    token = models.CharField(
        max_length=250,
        unique=True,  # اطمینان از منحصر به فرد بودن هر توکن
        verbose_name="توکن"
    )
    
    # فیلد برای ذخیره کد رمز یکبار مصرف (معمولاً یک رشته عددی)
    code = models.CharField(max_length=6, verbose_name="کد OTP")
    
    # فیلد برای ذخیره زمان انقضای رمز یکبار مصرف
    expiration = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="زمان انقضا"
    )
    
    # فیلد برای ذخیره زمان ایجاد رکورد رمز یکبار مصرف
    created = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    
    class Meta:
        verbose_name = "رمز یکبار مصرف"  # نام قابل خواندن برای مدل به صورت مفرد در فارسی
        verbose_name_plural = "رمزهای یکبار مصرف"  # نام قابل خواندن برای مدل به صورت جمع در فارسی
        
    # نمایش رشته‌ای مدل رمز یکبار مصرف
    def __str__(self):
        return f'{self.status}----{self.code}----{self.token}'
    
    # متدی برای محاسبه و تنظیم زمان انقضای رمز یکبار مصرف
    def get_expiration(self):
        created = self.created  # دریافت زمان ایجاد
        expiration = created + timezone.timedelta(minutes=2)  # تنظیم زمان انقضا به 2 دقیقه پس از ایجاد
        self.expiration = expiration  # به‌روزرسانی فیلد زمان انقضا
        self.save()  # ذخیره تغییرات در دیتابیس
        
    # متدی برای اعتبارسنجی وضعیت رمز یکبار مصرف بر اساس زمان انقضا
    def status_validation(self):
        if self.expiration <= timezone.now():  # بررسی اینکه آیا رمز یکبار مصرف منقضی شده است
            self.status = 'EXP'  # تنظیم وضعیت به منقضی شده
            return self.status
        else:
            return self.status  # بازگشت وضعیت فعلی




# مدل برای مدیریت ثبت نام کاربران همراه با تایید رمز یکبار مصرف
class UserRegisterOTP(models.Model):
    """
    مدل برای مدیریت ثبت نام کاربران همراه با تایید رمز یکبار مصرف.
    """

    # ارتباط خارجی با مدل رمز یکبار مصرف (OneTimePassword)
    otp = models.ForeignKey(
        OneTimePassword,  # مدل مرتبط
        on_delete=models.CASCADE,  # حذف داده مرتبط در صورت حذف رکورد اصلی
        related_name="registration_otps",  # نام مرتبط برای ارتباط معکوس
        verbose_name="ارجاع رمز یکبار مصرف"  # توضیح فیلد در رابط کاربری
    )

    # نام کاربری: نام یکتا برای ثبت نام کاربر
    username = models.CharField(
        max_length=40,  # حداکثر تعداد کاراکتر
        verbose_name="نام کاربری"  # توضیح فیلد در رابط کاربری
    )

    # ایمیل: ایمیل منحصر به فرد برای ثبت نام کاربر
    email = models.EmailField(
        verbose_name="ایمیل"  # توضیح فیلد در رابط کاربری
    )

    # رمز عبور: ذخیره هش رمز عبور به صورت موقت
    password = models.CharField(
        max_length=128,  # طول مجاز برای هش رمز عبور
        verbose_name="هش رمز عبور"  # توضیح فیلد در رابط کاربری
    )

    # نام و نام خانوادگی: ذخیره نام کامل کاربر (اختیاری)
    full_name = models.CharField(
        max_length=255,  # طول مجاز برای نام کامل
        verbose_name="نام و نام خانوادگی",  # توضیح فیلد در رابط کاربری
        null=True,  # اجازه مقدار خالی
        blank=True  # اجازه مقدار خالی در فرم‌ها
    )

    # زمان ایجاد: تاریخ ثبت رکورد برای ردیابی زمان ثبت نام
    created = models.DateTimeField(
        auto_now_add=True,  # ذخیره زمان ایجاد به صورت خودکار
        verbose_name="زمان ایجاد"  # توضیح فیلد در رابط کاربری
    )

    # متاداده‌های مدل: تنظیمات عمومی برای مدل
    class Meta:
        # نام مدل در رابط کاربری (مفرد)
        verbose_name = "رمز یکبار مصرف ثبت نام کاربر"
        # نام مدل در رابط کاربری (جمع)
        verbose_name_plural = "رمزهای یکبار مصرف ثبت نام کاربران"

    # نمایش رشته‌ای رکورد برای خوانایی بهتر
    def __str__(self):
        # بازگشت توضیح خلاصه‌ای از رکورد (نام کاربری و شماره تلفن مرتبط)
        return f"ثبت نام برای {self.username} - {self.otp.phone}"
