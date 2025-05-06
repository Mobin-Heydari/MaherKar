from rest_framework import serializers  # وارد کردن کتابخانه‌ی سریالایزرهای Django REST Framework برای تبدیل داده‌های مدل به JSON و برعکس
from .models import User, IdCardInFormation  # وارد کردن مدل‌های User و IdCardInFormation از فایل models در اپ فعلی




# تعریف سریالایزر برای مدل اطلاعات کارت ملی
class IdCardInFormationSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای اطلاعات کارت ملی
    """

    # مشخصات متادیتا برای سریالایزر
    class Meta:
        model = IdCardInFormation  # تعیین مدل مرتبط: IdCardInFormation
        fields = "__all__"  # استفاده از تمامی فیلدهای موجود در مدل

    # بازنویسی متد update جهت سفارشی‌سازی روند به‌روزرسانی نمونه‌های مدل
    def update(self, instance, validated_data):
        # دریافت شی request از context (برای دسترسی به اطلاعات کاربر مثلاً جهت بررسی سطح دسترسی)
        request = self.context.get('request')

        # در صورتی که کاربر درخواست‌کننده دارای سطح دسترسی ادمین باشد، امکان به‌روزرسانی وضعیت کارت وجود دارد
        if request.user.is_staff:
            # نکته: در این خط به اشتباه از عملگر مقایسه (==) استفاده شده است.
            # برای اختصاص مقدار صحیح باید از عملگر تخصیص (=) استفاده شود.
            instance.id_card_status == validated_data.get('id_card_status', instance.id_card_status)

        # به‌روزرسانی فیلد فایل کارت ملی؛ در صورتی که مقدار جدید ارسال شده باشد، در غیر این صورت مقدار قبلی حفظ می‌شود
        instance.id_card == validated_data.get('id_card', instance.id_card)
        # به‌روزرسانی فیلد شماره کارت ملی؛ در صورت ارسال مقدار جدید این فیلد به‌روزرسانی خواهد شد
        instance.id_card_number == validated_data.get('id_card_number', instance.id_card_number)

        # ذخیره‌ی تغییرات در نمونه مورد نظر به دیتابیس
        instance.save()
        # بازگرداندن نمونه به‌روزرسانی شده
        return instance



# تعریف سریالایزر برای مدل کاربر
class UserSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل کاربر
    """

    # درج سریالایزر مربوط به اطلاعات کارت ملی در فیلد مرتبط به id_card_info
    id_card_info = IdCardInFormationSerializer()

    # متادیتا برای سریالایزر مدل کاربر
    class Meta:
        model = User  # تعیین مدل مرتبط: User
        fields = [
            'id',                        # شناسه یکتا
            'id_card_info',              # اطلاعات کارت ملی کاربر به صورت تو در تو (nested)
            'full_name',                 # نام و نام خانوادگی
            'phone',                     # شماره تلفن
            'user_type',                 # نوع کاربر (برای مثال: جوینده کار، کارفرما، پشتیبان یا مدیر)
            'status',                    # وضعیت حساب کاربری (فعال، تعلیق شده یا حذف شده)
            'joined_date',               # تاریخ عضویت کاربر
            'last_updated',              # تاریخ آخرین به‌روزرسانی اطلاعات کاربر
        ]
        # تعیین فیلدهایی که فقط قابل خواندن هستند و تغییر نمی‌کنند
        read_only_fields = ['id', 'joined_date', 'last_updated', 'id_card_info']
    
    # بازنویسی متد update؛ در اینجا از پیاده‌سازی پیشفرض والد (ModelSerializer) استفاده شده است
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
