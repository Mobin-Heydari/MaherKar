from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager




class User(AbstractBaseUser, PermissionsMixin):
    # نوع‌های کاربر: تعریف نقش‌های مختلف برای کاربران
    class UserTypes(models.TextChoices):
        JOB_SEEKER = "JS", "جوینده کار"   # جوینده کار
        EMPLOYER = "EM", "کارفرما"         # کارفرما
        SUPPORT = "SU", "پشتیبان"         # پشتیبان
        ADMIN = "AD", "مدیر"              # مدیر سیستم

    # وضعیت احراز هویت دو مرحله‌ای
    class TwoFactorAuthenticationStatus(models.TextChoices):
        AUTHENTICATED = "A", "تایید شده"    # کاربری که احراز هویت شده است
        UNAUTHENTICATED = "UA", "تایید نشده" # کاربری که احراز هویت نشده است

    # وضعیت حساب کاربری
    class AccountStatus(models.TextChoices):
        ACTIVE = "ACT", "فعال"              # حساب فعال
        SUSPENDED = "SUS", "تعلیق شده"       # حساب تعلیق شده
        DELETED = "DEL", "حذف شده"           # حساب حذف شده

    # نوع کاربر: نقش یا دسته‌بندی کاربر (جوینده کار، کارفرما، و غیره)
    user_type = models.CharField(
        max_length=2,
        choices=UserTypes.choices,
        verbose_name="نوع کاربر",
    )

    # وضعیت احراز هویت دو مرحله‌ای: ذخیره وضعیت تایید هویت با نام شفاف‌تر
    two_factor_auth_status = models.CharField(
        max_length=2,
        choices=TwoFactorAuthenticationStatus.choices,
        default=TwoFactorAuthenticationStatus.UNAUTHENTICATED,
        verbose_name="وضعیت احراز هویت دو مرحله‌ای",
    )

    # زمان تایید آخرین احراز هویت دو مرحله‌ای
    tfa_verified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="زمان تایید احراز هویت دو مرحله‌ای",
    )

    # وضعیت حساب: وضعیت کلی حساب کاربر (فعال، تعلیق شده یا حذف شده)
    status = models.CharField(
        max_length=3,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
        verbose_name="وضعیت حساب کاربری",
    )

    # ایمیل کاربر: شناسه یکتای کاربر برای ورود به سیستم
    email = models.EmailField(
        unique=True,
        verbose_name="ایمیل",
    )

    # شماره تلفن کاربر: شماره تماس یکتا برای کاربر
    phone = models.CharField(
        unique=True,
        max_length=11,
        verbose_name="شماره تلفن",
    )

    # نام کاربری: نام منحصر به فردی که برای شناسایی کاربر استفاده می‌شود
    username = models.CharField(
        max_length=40,
        unique=True,
        verbose_name="نام کاربری",
    )

    # نام و نام خوانوادگی کاربر
    full_name = models.CharField(
        verbose_name="نام و نام خوانوادگی",
        max_length=255,
        null=True,
        blank=True,
    )

    # تاریخ عضویت: ذخیره تاریخ ثبت‌نام کاربر در سیستم
    joined_date = models.DateField(
        auto_now_add=True,
        verbose_name="تاریخ عضویت",
    )

    # تاریخ آخرین به‌روزرسانی حساب کاربری
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ آخرین به‌روزرسانی",
    )

    # وضعیت تایید ایمیل: بررسی تایید ایمیل کاربر
    email_verified = models.BooleanField(
        default=False,
        verbose_name="ایمیل تایید شده",
    )

    # وضعیت تایید شماره تلفن: بررسی تایید شماره تلفن کاربر
    phone_verified = models.BooleanField(
        default=False,
        verbose_name="شماره تلفن تایید شده",
    )

    # وضعیت فعال بودن کاربر: نشان‌دهنده فعال بودن حساب کاربر
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
    )

    # مدیر بودن کاربر: نشان‌دهنده اینکه آیا کاربر مدیر سیستم است یا خیر
    is_admin = models.BooleanField(
        default=False,
        verbose_name="مدیر",
    )

    # فیلد اصلی ورود: شماره تلفن به عنوان شناسه اصلی برای ورود به سیستم استفاده می‌شود
    USERNAME_FIELD = "phone"

    # فیلدهای ضروری برای ساخت کاربر جدید: علاوه بر شماره تلفن
    REQUIRED_FIELDS = ["username", "email", "full_name"]

    objects = UserManager()

    class Meta:
        ordering = ['joined_date']
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin
