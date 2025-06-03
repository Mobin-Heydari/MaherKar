from rest_framework import serializers

from .models import User




# تعریف سریالایزر برای مدل کاربر
class UserSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل کاربر
    """

    # متادیتا برای سریالایزر مدل کاربر
    class Meta:
        model = User  # تعیین مدل مرتبط: User
        fields = [
            'id',                        # شناسه یکتا
            'full_name',                 # نام و نام خانوادگی
            'phone',                     # شماره تلفن
            'user_type',                 # نوع کاربر (برای مثال: جوینده کار، کارفرما، پشتیبان یا مدیر)
            'status',                    # وضعیت حساب کاربری (فعال، تعلیق شده یا حذف شده)
            'joined_date',               # تاریخ عضویت کاربر
            'last_updated',              # تاریخ آخرین به‌روزرسانی اطلاعات کاربر
        ]
        # تعیین فیلدهایی که فقط قابل خواندن هستند و تغییر نمی‌کنند
        read_only_fields = ['id', 'joined_date', 'last_updated']
    
    # بازنویسی متد update؛ در اینجا از پیاده‌سازی پیشفرض والد (ModelSerializer) استفاده شده است
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
