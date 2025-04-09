from rest_framework import serializers  
# ایمپورت ماژول serializers از DRF جهت مدیریت داده‌های ورودی و خروجی سریالایزرها

from Advertisements.models import Advertisement  
# ایمپورت مدل Advertisement از اپ آگهی‌ها جهت ارتباط با آگهی در سفارش اشتراک

from Subscriptions.models import SubscriptionPlan, AdvertisementSubscription  
# ایمپورت مدل‌های SubscriptionPlan و AdvertisementSubscription از اپ اشتراک‌ها

from .models import SubscriptionOrder  
# ایمپورت مدل SubscriptionOrder از فایل models اپ سفارشات

import uuid  
# ایمپورت uuid جهت تولید شناسه‌های یکتا برای سفارشات



# =============================================================================
# سریالایزر SubscriptionOrderSerializer
# =============================================================================
class SubscriptionOrderSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل SubscriptionOrder جهت مدیریت داده‌های مربوط به سفارشات اشتراک.
    """

    class Meta:
        model = SubscriptionOrder  # اتصال سریالایزر به مدل SubscriptionOrder
        fields = "__all__"  # تمامی فیلدهای مدل در خروجی سریالایزر نمایش داده می‌شوند

    def create(self, validated_data):
        """
        متد create جهت ایجاد یک سفارش جدید بر اساس داده‌های ورودی.
        """
        # دریافت شیء request از context برای دسترسی به کاربر درخواست‌دهنده
        request = self.context.get('request')

        # استخراج شناسه طرح اشتراک (plan_id)، slug آگهی (ad_slug)، و شناسه اشتراک (subscription_id) از context
        plan_id = self.context.get('plan_id')
        ad_slug = self.context.get('ad_slug')
        subscription_id = self.context.get('subscription_id')
        
        # واکشی طرح اشتراک بر اساس شناسه plan_id
        plan = SubscriptionPlan.objects.get(id=plan_id)
        # واکشی آگهی بر اساس slug
        advertisement = Advertisement.objects.get(slug=ad_slug)
        # واکشی اشتراک آگهی بر اساس شناسه subscription_id
        subscription = AdvertisementSubscription.objects.get(id=subscription_id)

        # محاسبه قیمت روزانه اشتراک بر اساس طرح
        price = plan.price_per_day

        # دریافت مدت زمان اشتراک از داده‌های معتبر ورودی
        duration = validated_data.get('durations')

        # محاسبه قیمت کلی بر اساس مدت زمان و قیمت روزانه
        duration_price = duration * price
        # محاسبه مالیات (10٪ از قیمت کلی)
        taks_price = duration_price * 10 // 100

        # محاسبه قیمت نهایی
        total_price = duration_price + taks_price

        # تولید یک شناسه یکتا برای سفارش
        order_id = uuid.uuid4()

        # ایجاد یک نمونه جدید از SubscriptionOrder با اطلاعات محاسبه‌شده
        order = SubscriptionOrder.objects.create(
            plan=plan,
            owner=request.user,
            advertisement=advertisement,
            advertisement_subscription=subscription,
            total_price=total_price,
            duration=duration,
            order_id=order_id,
        )

        order.save()  # ذخیره نمونه ایجاد شده در دیتابیس
        return order  # بازگرداندن سفارش ایجاد شده
