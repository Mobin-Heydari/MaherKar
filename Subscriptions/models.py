from django.db import models
from django.utils import timezone


class SubscriptionPlan(models.Model):
    """
    مدل مربوط به طرح‌های اشتراک (مانند: پایه، پیشرفته).
    این مدل شامل اطلاعاتی مانند نام، توضیحات، قیمت روزانه، وضعیت فعال بودن،
    رایگان بودن طرح و زمان‌های ایجاد و بروزرسانی آن است.
    """
    name = models.CharField(max_length=100, verbose_name="نام طرح", unique=True)

    description = models.TextField(blank=True, verbose_name="توضیحات")

    price_per_day = models.BigIntegerField(verbose_name="قیمت روزانه")

    active = models.BooleanField(default=True, verbose_name="فعال")

    is_free = models.BooleanField(default=False, verbose_name="رایگانه؟")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return self.name


class AdvertisementSubscription(models.Model):
    """
    مدل اشتراک برای آگهی‌ها.
    این مدل اطلاعات مربوط به اشتراک یک آگهی را ذخیره می‌کند،
    شامل وضعیت اشتراک، طرح اشتراک، مدت زمان، تاریخ شروع و پایان، و تاریخ‌های ایجاد و به‌روزرسانی.
    """
    class SubscriptionStatus(models.TextChoices):
        DEFAULT = 'default', "پیش‌ فرض"
        SPECIAL = 'special', "خاص"

    subscription_status = models.CharField(
        max_length=30,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.DEFAULT,
        verbose_name="وضعیت اشتراک"
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.SET_NULL,
        related_name="subscriptions",
        verbose_name="طرح اشتراک",
        null=True,
        blank=True
    )

    duration = models.IntegerField(default=1, verbose_name="مدت زمان (روز)")

    start_date = models.DateTimeField(default=timezone.now, verbose_name="تاریخ شروع", null=True, blank=True)

    end_date = models.DateTimeField(verbose_name="تاریخ پایان", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
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
        return f"اشتراک آگهی برای {self.plan.name}"
