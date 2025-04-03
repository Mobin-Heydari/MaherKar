from django.db import models

from Advertisements.models import Advertisement
from Subscriptions.models import AdvertisementSubscription, SubscriptionPlan
from Users.models import User

import uuid




class SubscriptionOrder(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', "در انتظار"
        PAID = 'paid', "پرداخت شده"
        CANCELED = 'canceled', "لغو شده"
        FAILED = 'failed', "ناموفق"

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="مالک"
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        verbose_name="پلن"
    )

    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        verbose_name="آگهی"
    )

    advertisement_subscription = models.ForeignKey(
        AdvertisementSubscription,
        on_delete=models.CASCADE,
        verbose_name="اشتراک آکهی ها"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name="وضعیت پرداخت"
    )

    total_price = models.IntegerField(verbose_name="قیمت نهایی")

    order_id = models.UUIDField(verbose_name="آیدی", primary_key=True, default=uuid.uuid5)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "سفارش آگهی"
        verbose_name_plural = "سفارشات آگهی ها"

    
    def __str__(self):
        return 