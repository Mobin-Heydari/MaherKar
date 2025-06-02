from django.db import models  # ایمپورت کلاس‌های مدل از Django جهت تعریف مدل‌های دیتابیس

from Subscriptions.models import AdvertisementSubscription, SubscriptionPlan  
# ایمپورت مدل‌های AdvertisementSubscription و SubscriptionPlan از اپ اشتراک‌ها

from Users.models import User  # ایمپورت مدل User از اپ کاربران جهت اتصال مالک به سفارش

import uuid  # ایمپورت uuid برای تولید شناسه‌های یکتا برای سفارشات




# =============================================================================
# مدل SubscriptionOrder (سفارش اشتراک)
# =============================================================================
class SubscriptionOrder(models.Model):
    """
    مدل سفارش اشتراک، شامل اطلاعات مربوط به سفارش طرح‌های اشتراک،
    آگهی‌های مربوطه و وضعیت پرداخت.
    """

    # ---------------------------
    # کلاس داخلی PaymentStatus جهت تعیین وضعیت‌های پرداخت
    # ---------------------------
    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', "در انتظار"      # وضعیت پرداخت: در انتظار
        PAID = 'paid', "پرداخت شده"           # وضعیت پرداخت: پرداخت شده
        CANCELED = 'canceled', "لغو شده"      # وضعیت پرداخت: لغو شده
        FAILED = 'failed', "ناموفق"           # وضعیت پرداخت: ناموفق

    # ---------------------------
    # فیلدهای ارتباطی و کلیدی سفارش
    # ---------------------------
    owner = models.ForeignKey(
        User,                                  # ارتباط سفارش با مدل User جهت تعیین مالک سفارش
        on_delete=models.CASCADE,              # در صورت حذف مالک، رکورد سفارش نیز حذف می‌شود
        verbose_name="مالک"                     # عنوان فیلد در پنل ادمین
    )

    plan = models.ForeignKey(
        SubscriptionPlan,                      # ارتباط سفارش با مدل SubscriptionPlan جهت تعیین طرح اشتراک مربوطه
        on_delete=models.CASCADE,              # در صورت حذف طرح، رکورد سفارش نیز حذف می‌شود
        verbose_name="پلن"                      # عنوان فیلد در پنل ادمین
    )

    advertisement_subscription = models.ForeignKey(
        AdvertisementSubscription,             # ارتباط سفارش با مدل AdvertisementSubscription جهت تعیین اشتراک مربوطه
        on_delete=models.CASCADE,              # در صورت حذف اشتراک، رکورد سفارش نیز حذف می‌شود
        verbose_name="اشتراک آگهی ها"           # عنوان فیلد در پنل ادمین
    )

    # ---------------------------
    # فیلد وضعیت پرداخت
    # ---------------------------
    payment_status = models.CharField(
        max_length=20,                         # حداکثر طول مقدار ذخیره شده در دیتابیس (رشته‌ای)
        choices=PaymentStatus.choices,         # گزینه‌های موجود برای وضعیت پرداخت
        default=PaymentStatus.PENDING,         # مقدار پیش‌فرض: در انتظار
        verbose_name="وضعیت پرداخت"            # عنوان فیلد در پنل ادمین
    )

    # ---------------------------
    # سایر فیلدهای مرتبط با سفارش
    # ---------------------------
    durations = models.IntegerField(verbose_name="مدت زمان اشتراک", default=1)  
    # مدت زمان اشتراک بر حسب روز؛ مقدار پیش‌فرض 1 روز

    price = models.IntegerField(verbose_name="قیمت", default=0)  
    # قیمت واحد اشتراک؛ مقدار پیش‌فرض 0

    total_price = models.IntegerField(verbose_name="قیمت نهایی")  
    # قیمت نهایی بر اساس قیمت واحد ضربدر مدت زمان اشتراک

    order_id = models.UUIDField(verbose_name="آیدی", primary_key=True, default=uuid.uuid4)  
    # آیدی سفارش؛ به صورت UUID یکتا تولید می‌شود و به عنوان کلید اصلی تعریف شده است

    # ---------------------------
    # فیلدهای زمان‌بندی
    # ---------------------------
    created_at = models.DateTimeField(auto_now_add=True)  
    # زمان ایجاد سفارش؛ به صورت خودکار تنظیم می‌شود

    updated_at = models.DateTimeField(auto_now=True)  
    # زمان بروزرسانی سفارش؛ در هر تغییر به‌روز می‌شود

    class Meta:
        # تعیین نام نمایشی مفرد و جمع برای مدل در پنل ادمین
        verbose_name = "سفارش آگهی"
        verbose_name_plural = "سفارشات آگهی ها"

    def __str__(self):
        """
        متد __str__: نمایش نمایشی از سفارش.
        """
        return f"سفارش {self.order_id} - وضعیت: {self.payment_status}"  
        # نمایش شناسه سفارش و وضعیت پرداخت در خروجی
