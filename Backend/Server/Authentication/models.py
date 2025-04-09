from django.db import models  # ایمپورت ماژول مدل‌های Django جهت تعریف مدل‌های دیتابیس
from django.utils import timezone  # ایمپورت timezone جهت کار با تاریخ و زمان‌ها



# ==================================================================
# مدل OneTimePassword (رمز یکبار مصرف)
# ==================================================================
class OneTimePassword(models.Model):
    # تعریف یک کلاس داخلی با استفاده از TextChoices برای تعیین وضعیت‌های مجاز OTP
    class OtpStatus(models.TextChoices):
        EXPIRED = 'EXP', 'منقضی شده'  # وضعیت رمز: منقضی شده
        ACTIVE = 'ACT', 'فعال'         # وضعیت رمز: فعال

    # فیلدی برای ذخیره وضعیت (مثلاً فعال یا منقضی شده)
    status = models.CharField(
        verbose_name="وضعیت",          # توضیح فیلد به فارسی
        max_length=3,                  # حداکثر ۳ کاراکتر (مانند 'EXP' یا 'ACT')
        choices=OtpStatus.choices,     # استفاده از گزینه‌های تعریف شده در OtpStatus
        default=OtpStatus.ACTIVE       # مقدار پیش‌فرض: فعال
    )
    
    # فیلدی برای ذخیره توکن منحصربه‌فرد OTP
    token = models.CharField(
        max_length=250,                # حداکثر طول 250 کاراکتر
        unique=True,                   # توکن باید در کل دیتابیس یکتا باشد
        verbose_name="توکن"            # توضیح فیلد برای رابط کاربری
    )
    
    # فیلدی برای ذخیره کد OTP (به عنوان مثال، عدد 6 رقمی)
    code = models.CharField(
        max_length=6,                  # حداکثر ۶ کاراکتر
        verbose_name="کد OTP"          # توضیح فیلد
    )
    
    # فیلدی برای ذخیره تاریخ و زمان انقضای OTP
    expiration = models.DateTimeField(
        blank=True,                    # امکان خالی گذاشتن این فیلد در فرم‌ها
        null=True,                     # اجازه ذخیره مقدار NULL در دیتابیس
        verbose_name="زمان انقضا"       # توضیح فیلد به فارسی
    )
    
    # فیلدی برای ذخیره زمان ایجاد OTP (به صورت خودکار)
    created = models.DateTimeField(
        auto_now_add=True,             # به‌طور خودکار زمان ایجاد رکورد تنظیم می‌شود
        verbose_name="زمان ایجاد"      # توضیح فیلد
    )
    
    # متادیتا (Meta) جهت تنظیم نام‌های نمایشی مدل در پنل ادمین
    class Meta:
        verbose_name = "رمز یکبار مصرف"          # نام مفرد مدل به فارسی
        verbose_name_plural = "رمزهای یکبار مصرف" # نام جمع مدل به فارسی
        
    def __str__(self):
        # متد __str__ جهت نمایش خوانا از نمونه مدل؛ در اینجا وضعیت، کد و توکن نمایش داده می‌شود
        return f'{self.status}----{self.code}----{self.token}'
    
    def get_expiration(self):
        """
        محاسبه زمان انقضا:
         - این متد ۲ دقیقه به زمان ایجاد اضافه می‌کند تا زمان انقضا تعیین شود.
         - پس از محاسبه، فیلد expiration به‌روز شده و تغییرات ذخیره می‌شود.
        """
        created = self.created  # زمان ایجاد رکورد
        expiration = created + timezone.timedelta(minutes=2)  # اضافه کردن ۲ دقیقه به زمان ایجاد
        self.expiration = expiration  # تنظیم مقدار فیلد expiration
        self.save()  # ذخیره تغییرات در دیتابیس
        
    def status_validation(self):
        """
        اعتبارسنجی وضعیت OTP:
         - بررسی می‌کند که آیا زمان انقضا گذشته است یا خیر.
         - اگر گذشته باشد، وضعیت OTP به 'EXP' (منقضی شده) تغییر می‌کند.
         - در غیر این صورت، وضعیت فعلی برگردانده می‌شود.
        """
        if self.expiration <= timezone.now():  # مقایسه زمان انقضا با زمان فعلی
            self.status = 'EXP'  # تغییر وضعیت به منقضی شده
            return self.status
        else:
            return self.status


# ==================================================================
# مدل UserRegisterOTP (ثبت‌نام کاربران با استفاده از OTP)
# ==================================================================
class UserRegisterOTP(models.Model):
    """
    این مدل فرآیند ثبت‌نام کاربر همراه با تایید OTP را مدیریت می‌کند.
    اطلاعات کاربری و رمز یکبار مصرف ارسال‌شده در این مدل ذخیره و تایید می‌شود.
    """

    # ارتباط OneToOne با مدل OneTimePassword جهت ذخیره OTP مرتبط با ثبت‌نام
    otp = models.OneToOneField(
        OneTimePassword,               # مدل مرتبط
        on_delete=models.CASCADE,      # در صورت حذف OTP، رکورد ثبت‌نام نیز حذف خواهد شد
        related_name="registration_otps",  # نام رابطه معکوس جهت دسترسی از طرف OTP
        verbose_name="ارجاع رمز یکبار مصرف"  # توضیح فیلد
    )

    # فیلد برای ذخیره نام کاربری کاربر (شناسه ثبت‌نام)
    username = models.CharField(
        max_length=40,                 # حداکثر 40 کاراکتر
        verbose_name="نام کاربری"      # توضیح فیلد به فارسی
    )

    # فیلد برای ذخیره ایمیل کاربر
    email = models.EmailField(
        verbose_name="ایمیل"          # توضیح فیلد
    )

    # فیلد برای ذخیره شماره تلفن کاربر
    phone = models.CharField(
        verbose_name="شماره تلفن",     # توضیح فیلد
        max_length=11                  # حداکثر 11 کاراکتر
    )

    # فیلد برای ذخیره هش رمز عبور کاربر
    password = models.CharField(
        max_length=128,                # حداکثر طول هش رمز عبور
        verbose_name="هش رمز عبور"     # توضیح فیلد
    )

    # فیلد برای ذخیره نام کامل کاربر
    full_name = models.CharField(
        max_length=255,                # حداکثر 255 کاراکتر
        verbose_name="نام و نام خانوادگی"  # توضیح فیلد
    )

    # فیلدی برای ذخیره تکرار رمز عبور، جهت اعتبارسنجی در فرایند ثبت‌نام
    password_conf = models.CharField(
        max_length=255,                # حداکثر طول رشته
        verbose_name="تکرار رمزعبور"    # توضیح فیلد
    )

    # فیلدی برای ذخیره نوع کاربر؛ مقدار پیش‌فرض "JS" (مثلاً به معنای Job Seeker)
    user_type = models.CharField(
        max_length=2,                  # حداکثر 2 کاراکتر
        default="JS"                   # مقدار پیش‌فرض
    )

    # فیلد برای ذخیره زمان ایجاد رکورد ثبت‌نام (به صورت خودکار)
    created = models.DateTimeField(
        auto_now_add=True,             # تنظیم خودکار زمان هنگام ایجاد رکورد
        verbose_name="زمان ایجاد"      # توضیح فیلد
    )

    class Meta:
        verbose_name = "رمز یکبار مصرف ثبت نام کاربر"         # نام مفرد مدل به فارسی
        verbose_name_plural = "رمزهای یکبار مصرف ثبت نام کاربران"  # نام جمع مدل به فارسی

    def __str__(self):
        # متد __str__ برای نمایش خواندنی نمونه؛ در اینجا نام کاربری و توکن OTP نمایش داده می‌شود.
        return f"ثبت نام برای {self.username} - {self.otp.token}"
