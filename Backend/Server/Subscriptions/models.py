from django.db import models
from django.utils import timezone




class SubscriptionPlan(models.Model):
    """
    مدل مربوط به طرح‌های اشتراک (مانند: پایه، پیشرفته).
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
    """

    class SubscriptionStatus(models.TextChoices):
        DEFAULT = 'default', "پیش‌فرض"
        SPECIAL = 'special', "خاص"

    subscription_status = models.CharField(
        max_length=30,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.DEFAULT,
        verbose_name="وضعیت اشتراک"
    )

    plan = models.ForeignKey(
        'SubscriptionPlan',
        on_delete=models.SET_NULL,
        related_name="subscriptions",
        verbose_name="طرح اشتراک",
        null=True,
        blank=True
    )

    duration = models.IntegerField(default=1, verbose_name="مدت زمان (روز)")

    start_date = models.DateTimeField(default=timezone.now, verbose_name="تاریخ شروع")

    end_date = models.DateTimeField(verbose_name="تاریخ پایان")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "اشتراک آکهی"
        verbose_name_plural = "اشتراک های آگهی"


    def is_active(self):
        """
        بررسی وضعیت فعال بودن اشتراک بر اساس پرداخت و تاریخ انقضا.
        """
        return self.payment_status == self.PaymentStatus.PAID and timezone.now() < self.end_date


    def __str__(self):
        return f"اشتراک آگهی برای {self.plan.name}"

