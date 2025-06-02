from django.shortcuts import get_object_or_404  # تابع get_object_or_404 برای دریافت شیء یا برگرداندن خطای 404 در صورتی‌که شیء یافت نشود
from rest_framework import serializers          # وارد کردن سریالایزرهای Django REST Framework
from .models import Company                       # ایمپورت مدل Company از همین اپلیکیشن
from Users.models import User                      # ایمپورت مدل User برای دسترسی به اطلاعات کاربر (مدیرعامل)



# تعریف سریالایزر برای مدل شرکت
class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company  # مدل مرتبط
        # تعریف فیلدهایی که باید در خروجی سریالایزر گنجانده شوند
        fields = [
            'id',                 # شناسه یکتا
            'employer',           # مدیرعامل (کاربر مرتبط)
            'name',               # نام شرکت
            'description',        # توضیحات شرکت
            'website',            # آدرس وبسایت شرکت
            'email',              # ایمیل رسمی شرکت
            'phone_number',       # شماره تماس شرکت
            'logo',               # لوگوی شرکت
            'banner',             # بنر شرکت
            'intro_video',        # ویدئوی معرفی شرکت
            'address',            # آدرس فیزیکی شرکت
            'location',           # شهر یا محل شرکت (ارتباط با مدل City)
            'postal_code',        # کد پستی
            'founded_date',       # تاریخ تأسیس شرکت
            'industry',           # صنعتی که شرکت در آن فعالیت می‌کند
            'number_of_employees',# تعداد کارکنان شرکت
            'linkedin',           # لینک حساب LinkedIn شرکت
            'twitter',            # لینک حساب Twitter شرکت
            'instagram',          # لینک حساب Instagram شرکت
            'created_at',         # تاریخ ایجاد رکورد (خودکار)
            'updated_at'          # تاریخ آخرین به‌روزرسانی رکورد (خودکار)
        ]
        # تعیین فیلدهای read-only: این فیلدها توسط کاربر تغییر نمی‌کنند
        read_only_fields = ['employer', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        ایجاد نمونه جدید شرکت.
        در این متد، شناسه employer از context سریالایزر دریافت شده و کاربر مربوطه واکشی می‌شود.
        سپس شرکت با استفاده از داده‌های ورودی و کاربر بازیابی شده ایجاد می‌گردد.
        """
        # گرفتن شناسه مدیرعامل (employer_id) از context سریالایزر
        employer_id = self.context.get('employer_id')
        # بازیابی شیء کاربر با استفاده از employer_id؛ در صورت عدم وجود، خطای 404 صادر می‌شود
        employer = get_object_or_404(User, id=employer_id)

        # ایجاد نمونه‌ی شرکت با استفاده از داده‌های معتبر ورودی
        company = Company.objects.create(
            employer=employer,
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            website=validated_data.get('website'),
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            logo=validated_data.get('logo'),
            banner=validated_data.get('banner'),
            intro_video=validated_data.get('intro_video'),
            address=validated_data.get('address'),
            location=validated_data.get('location'),
            postal_code=validated_data.get('postal_code'),
            founded_date=validated_data.get('founded_date'),
            industry=validated_data.get('industry'),
            number_of_employees=validated_data.get('number_of_employees'),
            linkedin=validated_data.get('linkedin'),
            twitter=validated_data.get('twitter'),
            instagram=validated_data.get('instagram')
        )

        return company

    def update(self, instance, validated_data):
        """
        به‌روزرسانی نمونه‌ی موجود شرکت.
        فیلد employer به‌عنوان read-only تعریف شده و تغییر نخواهد کرد.
        سایر فیلدها با داده‌های ورودی به‌روز می‌شوند و سپس نمونه ذخیره می‌گردد.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.website = validated_data.get('website', instance.website)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.banner = validated_data.get('banner', instance.banner)
        instance.intro_video = validated_data.get('intro_video', instance.intro_video)
        instance.address = validated_data.get('address', instance.address)
        instance.location = validated_data.get('location', instance.location)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.founded_date = validated_data.get('founded_date', instance.founded_date)
        instance.industry = validated_data.get('industry', instance.industry)
        instance.number_of_employees = validated_data.get('number_of_employees', instance.number_of_employees)
        instance.linkedin = validated_data.get('linkedin', instance.linkedin)
        instance.twitter = validated_data.get('twitter', instance.twitter)
        instance.instagram = validated_data.get('instagram', instance.instagram)

        # ذخیره نمونه به‌روز شده در دیتابیس
        instance.save()
        return instance
