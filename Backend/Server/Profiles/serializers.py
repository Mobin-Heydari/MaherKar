# ایمپورت کردن ماژول‌های مورد نیاز از Django REST Framework
from rest_framework import serializers
# ایمپورت کردن مدل‌های مرتبط از اپلیکیشن‌های مورد نظر
from .models import (
    PersonalInformation,
    JobSeekerProfile,
    EmployerProfile,
    AdminProfile,
    SupportProfile
)




# -----------------------------
# سریالایزر برای مدل اطلاعات شخصی
# -----------------------------
class PersonalInformationSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای اطلاعات شخصی.
    این کلاس داده‌های مربوط به جنسیت، سن و تعداد فرزند را تبدیل به فرمت JSON می‌کند.
    """
    class Meta:
        # تعیین مدل مرتبط
        model = PersonalInformation
        # فیلدهایی که قرار است در سریالایزر استفاده شوند
        fields = ['gender', 'age', 'kids_count']
        # در صورتی که بخواهید به‌روزرسانی‌های مستقیم بر روی این فیلدها مجاز باشد،
        # می‌توانید گزینه read_only_fields را حذف کنید.
        # read_only_fields = []



# -----------------------------
# سریالایزر برای مدل پروفایل جوینده کار
# -----------------------------
class JobSeekerProfileSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل پروفایل جوینده کار.
    این سریالایزر شامل اطلاعات اصلی پروفایل به همراه بخش اطلاعات شخصی تو در تو می‌باشد.
    """
    # تعریف فیلد تو در تو برای اطلاعات شخصی؛
    # توجه داشته باشید که اگر read_only را حذف کنید، این فیلد قادر به دریافت داده‌های ورودی نیز خواهد بود.
    personal_info = PersonalInformationSerializer()

    class Meta:
        # تعیین مدل مرتبط
        model = JobSeekerProfile
        # فیلدهایی که در خروجی JSON گنجانده می‌شوند
        fields = '__all__'
        # برخی فیلدها تنها خواندنی هستند
        read_only_fields = ['created_at', 'updated_at']

    # متد به‌روزرسانی (update) برای پردازش داده‌های ورودی و اعمال تغییرات هم بر روی قسمت‌های تو در تو
    def update(self, instance, validated_data):
        # داده‌های مربوط به اطلاعات شخصی تو در تو را از داده‌های اصلی جدا می‌کنیم.
        personal_info_data = validated_data.pop('personal_info', None)
        
        # به‌روزرسانی فیلدهای اصلی پروفایل جوینده کار؛
        # با استفاده از setattr مقدار جدید را به هر فیلد نسبت می‌دهیم.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # ذخیره تغییرات در نمونه اصلی پروفایل
        instance.save()
    
        # اگر داده‌ای برای بخش اطلاعات شخصی موجود باشد، آن را به‌روزرسانی می‌کنیم.
        if personal_info_data:
            # فرض بر این است که instance.personal_info از قبل وجود دارد.
            personal_info_instance = instance.personal_info
            # به‌روزرسانی هر فیلد اطلاعات شخصی به صورت دستی.
            for attr, value in personal_info_data.items():
                setattr(personal_info_instance, attr, value)
            # ذخیره تغییرات اطلاعات شخصی
            personal_info_instance.save()
            
            # --- یا به صورت جایگزین، می‌توانیم از متد update سریالایزر اطلاعات شخصی استفاده کنیم:
            # serializer = PersonalInformationSerializer(personal_info_instance, data=personal_info_data, partial=True)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
    
        # بازگرداندن نمونه به‌روزرسانی شده
        return instance



# -----------------------------
# سریالایزر برای مدل پروفایل کارفرما
# -----------------------------
class EmployerProfileSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل پروفایل کارفرما.
    این سریالایزر اطلاعات شرکت، جزئیات کارفرما و اطلاعات شخصی مربوط به آن را شامل می‌شود.
    """
    # جهت جلوگیری از دریافت داده برای اطلاعات شخصی، فیلد به صورت read_only تعریف شده است
    personal_info = PersonalInformationSerializer(read_only=True)

    class Meta:
        model = EmployerProfile
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'user']

    # متد update جهت به‌روز‌رسانی پروفایل کارفرما، مشابه به پیاده‌سازی در پروفایل جوینده کار
    def update(self, instance, validated_data):
        # استخراج داده‌های مربوط به اطلاعات شخصی از داده‌های ورودی
        personal_info_data = validated_data.pop('personal_info', None)
        
        # به‌روزرسانی فیلدهای اصلی پروفایل کارفرما به صورت دستی
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
    
        # در صورت وجود داده‌های تو در تو برای اطلاعات شخصی، آن‌ها به‌روزرسانی می‌شوند.
        if personal_info_data:
            personal_info_instance = instance.personal_info
            for attr, value in personal_info_data.items():
                setattr(personal_info_instance, attr, value)
            personal_info_instance.save()
            
            # --- یا می‌توانید از متد update سریالایزر اطلاعات شخصی استفاده کنید:
            # serializer = PersonalInformationSerializer(personal_info_instance, data=personal_info_data, partial=True)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
    
        return instance



# -----------------------------
# سریالایزر برای مدل پروفایل مدیر
# -----------------------------
class AdminProfileSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل پروفایل مدیر.
    این سریالایزر اطلاعات مدیر از جمله کاربر مرتبط و تاریخ‌های ایجاد و به‌روزرسانی را شامل می‌شود.
    """
    class Meta:
        model = AdminProfile
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']



# -----------------------------
# سریالایزر برای مدل پروفایل پشتیبان
# -----------------------------
class SupportProfileSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل پروفایل پشتیبان.
    این سریالایزر شامل اطلاعات مرتبط با کاربر پشتیبان و تاریخ‌های ساخت و به‌روزرسانی آن می‌شود.
    """
    class Meta:
        model = SupportProfile
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
