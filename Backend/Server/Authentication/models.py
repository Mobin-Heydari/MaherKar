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
