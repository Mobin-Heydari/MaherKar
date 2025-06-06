from rest_framework import serializers
from .models import SubscriptionPlan, AdvertisementSubscription




class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """
    سریالایزر مربوط به مدل SubscriptionPlan که شامل فیلدهای مربوط به طرح اشتراک است.
    """

    class Meta:
        model = SubscriptionPlan
        fields = [
            "id",
            "name",
            "description",
            "price_per_day",
            "active",
            "is_free",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

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
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.price_per_day = validated_data.get("price_per_day", instance.price_per_day)
        instance.active = validated_data.get("active", instance.active)

        instance.save()
        return instance


class AdvertisementSubscriptionSerializer(serializers.ModelSerializer):
    """
    سریالایزر مربوط به مدل AdvertisementSubscription که اطلاعات اشتراک آگهی را مدیریت می‌کند.
    """
    plan = SubscriptionPlanSerializer(read_only=True)

    class Meta:
        model = AdvertisementSubscription
        fields = "__all__"
