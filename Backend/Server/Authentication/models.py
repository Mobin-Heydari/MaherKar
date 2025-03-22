from django.db import models  # ایمپورت ماژول مدل‌ها برای تعریف مدل‌های دیتابیس
from django.utils import timezone  # ایمپورت timezone برای کار با زمان‌ها و تاریخ‌ها


# تعریف مدل برای رمز یکبار مصرف
class OneTimePassword(models.Model):
    # تعریف یک کلاس داخلی برای حالت‌های رمز یکبار مصرف با استفاده از TextChoices
    class OtpStatus(models.TextChoices):
        EXPIRED = 'EXP', 'منقضی شده'  # حالت رمز منقضی شده
        ACTIVE = 'ACT', 'فعال'         # حالت رمز فعال
    
    # فیلدی برای ذخیره وضعیت رمز یکبار مصرف
    status = models.CharField(
        verbose_name="وضعیت",  # توضیح فیلد به زبان فارسی
        max_length=3,  # حداکثر طول مقدار ذخیره شده
        choices=OtpStatus.choices,  # لیست انتخاب برای وضعیت رمز
        default=OtpStatus.ACTIVE  # مقدار پیش‌فرض: رمز فعال
    )
    
    # فیلدی برای ذخیره توکن منحصربه‌فرد رمز یکبار مصرف
    token = models.CharField(
        max_length=250,  # حداکثر طول رشته
        unique=True,  # مشخص کردن اینکه توکن باید منحصربه‌فرد باشد
        verbose_name="توکن"  # توضیح فیلد برای رابط کاربری
    )
    
    # فیلدی برای ذخیره کد رمز یکبار مصرف
    code = models.CharField(
        max_length=6,  # طول مجاز برای کد OTP
        verbose_name="کد OTP"  # توضیح فیلد به فارسی
    )
    
    # فیلدی برای ذخیره تاریخ و زمان انقضای رمز
    expiration = models.DateTimeField(
        blank=True,  # اجازه دادن به مقدار خالی
        null=True,  # اجازه دادن به مقدار null
        verbose_name="زمان انقضا"  # توضیح برای رابط کاربری
    )
    
    # فیلدی برای ذخیره زمان ایجاد رکورد
    created = models.DateTimeField(
        auto_now_add=True,  # تنظیم خودکار زمان هنگام ایجاد رکورد
        verbose_name="زمان ایجاد"  # توضیح فیلد به فارسی
    )
    
    # تعریف متادیتا برای تغییر نام مدل‌ها در رابط کاربری
    class Meta:
        verbose_name = "رمز یکبار مصرف"  # نام فارسی مفرد
        verbose_name_plural = "رمزهای یکبار مصرف"  # نام فارسی جمع
        
    # متدی برای نمایش رشته‌ای از شیء مدل
    def __str__(self):
        # نمایش وضعیت، کد، و توکن
        return f'{self.status}----{self.code}----{self.token}'
    
    # متدی برای محاسبه زمان انقضا و تنظیم آن
    def get_expiration(self):
        created = self.created  # زمان ایجاد رکورد
        expiration = created + timezone.timedelta(minutes=2)  # اضافه کردن ۲ دقیقه به زمان ایجاد
        self.expiration = expiration  # تنظیم مقدار جدید برای زمان انقضا
        self.save()  # ذخیره تغییرات در دیتابیس
        
    # متدی برای بررسی وضعیت رمز و اعتبارسنجی آن
    def status_validation(self):
        if self.expiration <= timezone.now():  # اگر زمان انقضا گذشته باشد
            self.status = 'EXP'  # تغییر وضعیت به منقضی شده
            return self.status  # بازگشت وضعیت
        else:
            return self.status  # بازگشت وضعیت فعلی


# تعریف مدل برای ثبت‌نام کاربران و تایید رمز یکبار مصرف
class UserRegisterOTP(models.Model):
    """
    این مدل مسئول مدیریت فرآیند ثبت‌نام کاربران همراه با تایید رمز یکبار مصرف است.
    """

    # اتصال این مدل به مدل رمز یکبار مصرف با استفاده از ارتباط OneToOne
    otp = models.OneToOneField(
        OneTimePassword,  # مدل مرتبط
        on_delete=models.CASCADE,  # حذف رکورد مرتبط در صورت حذف این رکورد
        related_name="registration_otps",  # نام ارتباط معکوس
        verbose_name="ارجاع رمز یکبار مصرف"  # توضیح فیلد به فارسی
    )

    # ذخیره نام کاربری برای کاربر
    username = models.CharField(
        max_length=40,  # حداکثر طول نام کاربری
        verbose_name="نام کاربری"  # توضیح برای رابط کاربری
    )

    # ذخیره ایمیل کاربر
    email = models.EmailField(
        verbose_name="ایمیل"  # توضیح فیلد به فارسی
    )

    # ذخیره شماره تلفن کاربر
    phone = models.CharField(
        verbose_name="شماره تلفن",  # توضیح فیلد برای رابط کاربری
        max_length=11  # حداکثر طول شماره تلفن
    )

    # ذخیره رمز عبور (به صورت هش)
    password = models.CharField(
        max_length=128,  # حداکثر طول هش رمز عبور
        verbose_name="هش رمز عبور"  # توضیح فیلد
    )

    # ذخیره نام کامل کاربر
    full_name = models.CharField(
        max_length=255,  # حداکثر طول نام کامل
        verbose_name="نام و نام خانوادگی"  # توضیح فیلد برای رابط کاربری
    )

    # فیلدی برای ذخیره تکرار رمز عبور
    password_conf = models.CharField(
        max_length=255,  # حداکثر طول رشته
        verbose_name="تکرار رمزعبور"  # توضیح به فارسی
    )

    # نوع کاربر (به صورت پیش‌فرض "JS")
    user_type = models.CharField(
        max_length=2,  # حداکثر طول
        default="JS"  # مقدار پیش‌فرض
    )

    # زمان ایجاد رکورد ثبت‌نام
    created = models.DateTimeField(
        auto_now_add=True,  # تنظیم زمان ایجاد به صورت خودکار
        verbose_name="زمان ایجاد"  # توضیح به فارسی
    )

    # متادیتا برای تغییر نام مدل‌ها در رابط کاربری
    class Meta:
        verbose_name = "رمز یکبار مصرف ثبت نام کاربر"  # نام فارسی مفرد
        verbose_name_plural = "رمزهای یکبار مصرف ثبت نام کاربران"  # نام فارسی جمع

    # متدی برای نمایش رشته‌ای از اطلاعات مدل
    def __str__(self):
        # نمایش نام کاربری و توکن رمز
        return f"ثبت نام برای {self.username} - {self.otp.token}"
