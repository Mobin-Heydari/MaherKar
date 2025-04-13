from django.utils.text import slugify  # تابع slugify برای تبدیل رشته به اسلاگ (رشته‌ای URL-friendly)
from django.shortcuts import get_object_or_404  # تابع get_object_or_404 جهت بازیابی شیء از دیتابیس یا برگرداندن خطای 404 اگر شیء یافت نشود
from rest_framework import serializers  # وارد کردن ماژول سریالایزرهای Django REST Framework
from .models import Province, City  # ایمپورت مدل‌های Province و City از فایل models



# ========================================================
# سریالایزر استان (ProvinceSerializer)
# ========================================================
class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province  # مدل مرتبط این سریالایزر، Province است
        fields = ('id', 'name', 'slug')  # فیلدهایی که باید در خروجی نمایش داده شوند

    def create(self, validated_data):
        """
        متد create به منظور ایجاد نمونه‌ای جدید از Province اجرا می‌شود.
        این متد:
          - ابتدا نام استان را از داده‌های معتبر شده استخراج می‌کند.
          - سپس با استفاده از تابع slugify (با پارامتر allow_unicode=True) یک اسلاگ از نام تولید می‌کند.
          - در نهایت نمونه جدید استان با استفاده از داده‌های name و slug ایجاد و برگردانده می‌شود.
        """
        # دریافت نام استان از داده‌های معتبر شده
        name = validated_data.get('name')
        # تولید اسلاگ از نام، با اجازه کاراکترهای یونیکد
        slug = slugify(name, allow_unicode=True)
        # ایجاد نمونه استان با نام و اسلاگ تولید شده
        province = Province.objects.create(name=name, slug=slug)
        return province

    def update(self, instance, validated_data):
        """
        متد update جهت بروزرسانی نمونه موجود از Province پیاده‌سازی شده است.
        در این متد:
          - در صورت دریافت نام جدید برای استان، مقدار آن به‌روزرسانی می‌شود؛ در غیر اینصورت مقدار قبلی حفظ می‌شود.
          - اسلاگ نیز بر اساس نام جدید بروزرسانی می‌شود.
          - در انتها نمونه به‌روزرسانی شده ذخیره و برگردانده می‌شود.
        """
        # به‌روزرسانی فیلد name، در صورتی که مقدار جدیدی دریافت شده باشد
        instance.name = validated_data.get('name', instance.name)
        # بروزرسانی اسلاگ جدید بر اساس نام به‌روز شده (با allow_unicode=True)
        instance.slug = slugify(instance.name, allow_unicode=True)
        instance.save()  # ذخیره نمونه به‌روز شده در دیتابیس
        return instance


# ========================================================
# سریالایزر شهر (CitySerializer)
# ========================================================
class CitySerializer(serializers.ModelSerializer):
    # نمایش جزئیات استان مرتبط به صورت تو در تو (nested) به صورت read-only
    province_detail = ProvinceSerializer(source='province', read_only=True)

    class Meta:
        model = City  # مدل مرتبط این سریالایزر، City است
        # فیلدهایی که در خروجی نمایش داده می‌شوند؛ province_detail اطلاعات استان مرتبط را نشان می‌دهد
        fields = ('id', 'name', 'slug', 'province_detail')

    def create(self, validated_data):
        """
        متد create برای ایجاد یک نمونه جدید از City پیاده‌سازی می‌شود.
        این متد به صورت زیر عمل می‌کند:
          - انتظار دارد که در context سریالایزر، مقدار 'province_slug' وجود داشته باشد.
          - اگر این کلید موجود نباشد، یک خطای اعتبارسنجی صادر می‌کند.
          - با استفاده از get_object_or_404، استان مرتبط با اسلاگ داده‌شده واکشی می‌شود.
          - نام شهر از داده‌های ورودی استخراج شده و از آن یک اسلاگ تولید می‌شود.
          - در نهایت یک نمونۀ جدید City با اتصال به استان واکشی‌شده ایجاد می‌شود.
        """
        # دریافت اسلاگ استان از context؛ این مقدار باید توسط view یا منبع دیگر در context قرار داده شود
        province_slug = self.context.get('province_slug')
        if not province_slug:
            raise serializers.ValidationError({"province_slug": "Slug of the province is required."})
        
        # واکشی شی Province مطابق با اسلاگ
        province = get_object_or_404(Province, slug=province_slug)
        # استخراج نام شهر از داده‌های معتبر شده
        name = validated_data.get('name')
        # تولید اسلاگ از نام شهر با اجازه کاراکترهای یونیکد
        slug = slugify(name, allow_unicode=True)
        # ایجاد نمونه جدید City با اتصال به استان پیدا شده
        city = City.objects.create(province=province, name=name, slug=slug)
        return city

    def update(self, instance, validated_data):
        """
        متد update جهت به‌روزرسانی نمونه موجود از City.
          - ابتدا بررسی می‌کند که آیا در context یک province_slug جدید ارسال شده است.
          - اگر ارسال شده باشد، استان جدید بر اساس آن اسلاگ واکشی شده و نمونه به‌روزرسانی می‌شود.
          - سپس نام شهر (و در نتیجه اسلاگ تولید شده) بر اساس داده‌های ورودی به‌روزرسانی می‌شود.
        """
        # دریافت یک province_slug جدید از context (در صورتی که ارسال شده باشد)
        province_slug = self.context.get('province_slug')
        if province_slug:
            # واکشی استان جدید مطابق با اسلاگ
            province = get_object_or_404(Province, slug=province_slug)
            instance.province = province  # به‌روزرسانی فیلد province

        # به‌روزرسانی نام شهر؛ در صورت ارسال مقدار جدید، استفاده می‌شود
        instance.name = validated_data.get('name', instance.name)
        # تولید اسلاگ جدید بر اساس نام به‌روز شده
        instance.slug = slugify(instance.name, allow_unicode=True)
        instance.save()  # ذخیره تغییرات در دیتابیس
        return instance
