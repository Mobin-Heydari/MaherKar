from django.db import models

from Advertisements.models import Advertisement

from Subscriptions.models import AdvertisementSubscription, SubscriptionPlan

from Users.models import User

import uuid



class SubscriptionOrder(models.Model):
    """
    مدل سفارش اشتراک، شامل اطلاعات مربوط به سفارش طرح‌های اشتراک،
    آگهی‌های مربوطه و وضعیت پرداخت.
    """

    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', "در انتظار"
        PAID = 'paid', "پرداخت شده"
        CANCELED = 'canceled', "لغو شده"
        FAILED = 'failed', "ناموفق"
    
    class TypeChoices(models.TextChoices):
        JOB = 'J', 'شغل'
        RESUME = 'R', 'رزومه'


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="مالک",
        related_name="user_subscription_orders"
    )

    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name="advertisement_orders"
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        verbose_name="پلن",
        related_name="plan_orders"
    )

    subscription = models.ForeignKey(
        AdvertisementSubscription,
        on_delete=models.CASCADE,
        verbose_name="اشتراک آگهی ها",
        related_name="subscription_orders"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name="وضعیت پرداخت"
    )

    ad_type = models.CharField(
        max_length=1,
        verbose_name="نوع آگهی",
        choices=TypeChoices.choices,
    )

    durations = models.IntegerField(verbose_name="مدت زمان اشتراک", default=1)

    price = models.IntegerField(verbose_name="قیمت", default=0)
    
    total_price = models.IntegerField(verbose_name="قیمت نهایی")


    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        # تعیین نام نمایشی مفرد و جمع برای مدل در پنل ادمین
        verbose_name = "سفارش آگهی"
        verbose_name_plural = "سفارشات آگهی ها"

    def __str__(self):
        """
        متد __str__: نمایش نمایشی از سفارش.
        """
        return f"سفارش {self.order_id} - وضعیت: {self.payment_status}"