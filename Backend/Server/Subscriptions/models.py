from django.db import models  # ایمپورت مدل‌های Django جهت تعریف مدل‌های دیتابیس
from django.utils import timezone  # ایمپورت timezone جهت کار با تاریخ و زمان



# =============================================================================
# مدل SubscriptionPlan (طرح‌های اشتراک)
# =============================================================================
class SubscriptionPlan(models.Model):
    """
    مدل مربوط به طرح‌های اشتراک (مانند: پایه، پیشرفته).
    این مدل شامل اطلاعاتی مانند نام، توضیحات، قیمت روزانه، وضعیت فعال بودن،
    رایگان بودن طرح و زمان‌های ایجاد و بروزرسانی آن است.
    """

    # فیلد نام طرح؛ کاربر باید نامی یکتا برای هر طرح وارد کند.
    name = models.CharField(max_length=100, verbose_name="نام طرح", unique=True)

    # فیلد توضیحات؛ امکان خالی گذاشتن آن فراهم شده است.
    description = models.TextField(blank=True, verbose_name="توضیحات")

    # فیلد قیمت روزانه؛ قیمت طرح را به صورت عدد صحیح بزرگ ذخیره می‌کند.
    price_per_day = models.BigIntegerField(verbose_name="قیمت روزانه")

    # فیلد active جهت مشخص کردن اینکه طرح فعال است یا خیر؛ به صورت بولی تعریف شده.
    active = models.BooleanField(default=True, verbose_name="فعال")
    # فیلد is_free جهت مشخص کردن اینکه طرح رایگان است یا خیر.
    is_free = models.BooleanField(default=False, verbose_name="رایگانه؟")

    # فیلد زمان ایجاد؛ به صورت خودکار زمان ایجاد رکورد ثبت می‌شود.
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    # فیلد زمان بروزرسانی؛ به صورت خودکار در هر تغییر زمان بروزرسانی شده ذخیره می‌شود.
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        # متد __str__، نام طرح اشتراک را برمی‌گرداند تا در نمایش‌های متنی استفاده شود.
        return self.name


# =============================================================================
# مدل AdvertisementSubscription (اشتراک آگهی‌ها)
# =============================================================================
class AdvertisementSubscription(models.Model):
    """
    مدل اشتراک برای آگهی‌ها.
    این مدل اطلاعات مربوط به اشتراک یک آگهی را ذخیره می‌کند،
    شامل وضعیت اشتراک، طرح اشتراک، مدت زمان، تاریخ شروع و پایان، و تاریخ‌های ایجاد و به‌روزرسانی.
    """

    # کلاس داخلی جهت تعریف گزینه‌های وضعیت اشتراک با استفاده از TextChoices
    class SubscriptionStatus(models.TextChoices):
        DEFAULT = 'default', "پیش‌ فرض"  # وضعیت پیش‌فرض اشتراک
        SPECIAL = 'special', "خاص"       # وضعیت ویژه اشتراک

    # فیلد وضعیت اشتراک؛ مقدار آن از گزینه‌های تعریف شده در SubscriptionStatus انتخاب می‌شود.
    subscription_status = models.CharField(
        max_length=30,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.DEFAULT,
        verbose_name="وضعیت اشتراک"
    )

    # فیلد plan؛ ارتباط یک به چند با مدل SubscriptionPlan.
    # در صورت حذف طرح مربوطه، مقدار این فیلد به NULL تنظیم می‌شود.
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.SET_NULL,
        related_name="subscriptions",
        verbose_name="طرح اشتراک",
        null=True,
        blank=True
    )

    # فیلد duration؛ مدت زمان (بر حسب روز) اشتراک را ذخیره می‌کند.
    duration = models.IntegerField(default=1, verbose_name="مدت زمان (روز)")

    # فیلد start_date؛ تاریخ شروع اشتراک را تنظیم می‌کند.
    start_date = models.DateTimeField(default=timezone.now, verbose_name="تاریخ شروع")

    # فیلد end_date؛ تاریخ پایان اشتراک را ذخیره می‌کند.
    end_date = models.DateTimeField(verbose_name="تاریخ پایان")

    # فیلد created_at؛ تاریخ ایجاد رکورد اشتراک به‌صورت خودکار تنظیم می‌شود.
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    # فیلد updated_at؛ تاریخ آخرین بروزرسانی رکورد اشتراک به‌طور خودکار ذخیره می‌شود.
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        # تعریف نام نمایشی مفرد و جمع مدل در پنل ادمین
        verbose_name = "اشتراک آگهی"
        verbose_name_plural = "اشتراک های آگهی"

    def is_active(self):
        """
        بررسی وضعیت فعال بودن اشتراک بر اساس پرداخت و تاریخ انقضا.
        این متد بررسی می‌کند که آیا وضعیت پرداخت برابر با PAID است و تاریخ فعلی قبل از تاریخ پایان اشتراک می‌باشد.
        توجه: فیلد payment_status و PaymentStatus در کد تعریف نشده‌اند؛ بنابراین فرض بر این است که باید تعریف شوند.
        """
        return self.payment_status == self.PaymentStatus.PAID and timezone.now() < self.end_date

    def __str__(self):
        # متد __str__، یک رشته نمایشی شامل نام طرح اشتراک مربوط به این اشتراک آگهی برمی‌گرداند.
        return f"اشتراک آگهی برای {self.plan.name}"
