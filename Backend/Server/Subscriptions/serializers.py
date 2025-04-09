from rest_framework import serializers  
# ایمپورت ماژول serializers از DRF برای تعریف و مدیریت سریالایزرها

from .models import SubscriptionPlan, AdvertisementSubscription  
# ایمپورت مدل‌های SubscriptionPlan و AdvertisementSubscription جهت استفاده در سریالایزرها



# =============================================================================
# سریالایزر SubscriptionPlanSerializer (طرح‌های اشتراک)
# =============================================================================
class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """
    سریالایزر مربوط به مدل SubscriptionPlan که شامل فیلدهای مربوط به طرح اشتراک است.
    """

    class Meta:
        model = SubscriptionPlan  # اتصال سریالایزر به مدل SubscriptionPlan
        fields = ['id', 'name', 'description', 'price_per_day', 'active', 'is_free', 'created_at', 'updated_at']  
        # فیلدهایی که در خروجی نمایش داده خواهند شد
        read_only_fields = ['id', 'created_at', 'updated_at']  
        # فیلدهایی که فقط خواندنی هستند و قابل تغییر نیستند

    def create(self, validated_data):
        """
        متد ایجاد یک نمونه جدید از SubscriptionPlan.
        validated_data داده‌های معتبر دریافت شده از ورودی هستند.
        """
        return SubscriptionPlan.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        متد به‌روزرسانی یک نمونه موجود از SubscriptionPlan.
        داده‌های ورودی با مقادیر فعلی نمونه ادغام شده و ذخیره می‌شوند.
        """
        # به‌روزرسانی مقدار نام طرح اگر مقدار جدید وارد شده باشد
        instance.name = validated_data.get('name', instance.name)
        # به‌روزرسانی توضیحات طرح
        instance.description = validated_data.get('description', instance.description)
        # به‌روزرسانی قیمت روزانه طرح
        instance.price_per_day = validated_data.get('price_per_day', instance.price_per_day)
        # به‌روزرسانی وضعیت فعال بودن طرح
        instance.active = validated_data.get('active', instance.active)

        instance.save()  # ذخیره تغییرات در دیتابیس
        return instance  # بازگرداندن نمونه به‌روزرسانی‌شده


# =============================================================================
# سریالایزر AdvertisementSubscriptionSerializer (اشتراک آگهی‌ها)
# =============================================================================
class AdvertisementSubscriptionSerializer(serializers.ModelSerializer):
    """
    سریالایزر مربوط به مدل AdvertisementSubscription که اطلاعات اشتراک آگهی را مدیریت می‌کند.
    """
    # نمایش اطلاعات طرح اشتراک مربوطه با استفاده از SubscriptionPlan
    plan = SubscriptionPlan()

    class Meta:
        model = AdvertisementSubscription  # اتصال سریالایزر به مدل AdvertisementSubscription
        fields = "__all__"  # تمامی فیلدهای مدل AdvertisementSubscription در خروجی نمایش داده می‌شوند
