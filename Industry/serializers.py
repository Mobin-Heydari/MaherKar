from django.shortcuts import get_object_or_404  # برای بازیابی شیء و ارسال خطای 404 در صورت عدم وجود
from rest_framework import serializers          # وارد کردن کتابخانه سریالایزرهای DRF
from .models import Industry, IndustryCategory, Skill  # ایمپورت مدل‌های مربوطه




# ===============================
# سریالایزر دسته‌بندی صنایع (IndustryCategorySerializer)
# ===============================
class IndustryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryCategory  # مدل مرتبط: IndustryCategory
        fields = [
            'id',       # شناسه یکتا
            'name',     # نام دسته‌بندی
            'slug',     # اسلاگ دسته‌بندی که به صورت URL-friendly تولید می‌شود
        ]
        read_only_fields = ['slug']  # فیلد slug فقط خواندنی است؛ تولید آن به صورت خودکار انجام می‌شود

    def create(self, validated_data):
        """
        ایجاد یک نمونه جدید از دسته‌بندی.
        اسلاگ به صورت خودکار در متد save مدل تولید می‌شود.
        """
        # دریافت نام از داده‌های معتبر شده
        name = validated_data.get('name')
        # ایجاد نمونه‌ی جدید دسته‌بندی فقط با فیلد name؛ سایر فیلد مانند slug در متد save تولید می‌شوند.
        category = IndustryCategory.objects.create(name=name)
        return category

    def update(self, instance, validated_data):
        """
        به‌روزرسانی نمونه‌ی موجود دسته‌بندی.
        """
        # به‌روزرسانی فیلد name؛ اگر مقدار جدید ارائه نشده باشد مقدار قبلی حفظ می‌شود.
        instance.name = validated_data.get('name', instance.name)
        # ذخیره تغییرات
        instance.save()
        return instance


# ===============================
# سریالایزر صنایع (IndustrySerializer)
# ===============================
class IndustrySerializer(serializers.ModelSerializer):
    # اضافه کردن فیلد category_name جهت نمایش نام دسته‌بندی مرتبط؛ خواندنی
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Industry  # مدل مرتبط: Industry
        fields = [
            'id',          # شناسه یکتا
            'name',        # نام صنعت
            'slug',        # اسلاگ صنعت (تولید خودکار در مدل)
            'category',    # شناسه دسته‌بندی (ForeignKey)
            'category_name' # نام دسته‌بندی برای نمایش
        ]
        read_only_fields = ['slug']  # فیلد slug تنها خواندنی است

    def create(self, validated_data):
        """
        ایجاد یک نمونه جدید از صنعت و اتصال آن به دسته‌بندی مرتبط.
        برای این کار، اسلاگ دسته‌بندی از context دریافت شده و دسته‌بندی مربوطه واکشی می‌شود.
        """
        # دریافت category_slug از context؛ در صورتی که وجود نداشته باشد، اعتبارسنجی خطا خواهد داد.
        category_slug = self.context.get('category_slug')
        if not category_slug:
            raise serializers.ValidationError({"category_slug": "Slug of the category is required."})
        
        # واکشی دسته‌بندی با استفاده از slug
        category = get_object_or_404(IndustryCategory, slug=category_slug)

        # ایجاد صنعت جدید با نام و دسته‌بندی واکشی شده
        industry = Industry.objects.create(
            name=validated_data.get('name'),
            category=category,
        )
        return industry

    def update(self, instance, validated_data):
        """
        به‌روزرسانی نمونه موجود از صنعت.
        """
        # به‌روز‌رسانی نام صنعت یا نگهداری مقدار قبلی در صورت عدم ارائه مقدار جدید
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


# ===============================
# سریالایزر مهارت‌ها (SkillSerializer)
# ===============================
class SkillSerializer(serializers.ModelSerializer):
    # نمایش جزئیات صنعت به‌عنوان فیلد تو در تو در نمایش مهارت؛ خواندنی است.
    industry = IndustrySerializer(read_only=True)
    
    class Meta:
        model = Skill  # مدل مرتبط: Skill
        fields = ('id', 'name', 'icon', 'industry')
    
    def create(self, validated_data):
        """
        ایجاد یک نمونه جدید از مهارت و اختصاص آن به یک صنعت.
        برای این منظور، industry_slug از context دریافت شده و صنعت مربوطه واکشی می‌شود.
        """
        # دریافت industry_slug از context؛ در صورت عدم وجود خطای اعتبارسنجی می‌دهد.
        industry_slug = self.context.get('industry_slug')
        if not industry_slug:
            raise serializers.ValidationError({"industry_slug": "Slug of the industry is required."})
        
        # واکشی صنعت با استفاده از اسلاگ
        industry = get_object_or_404(Industry, slug=industry_slug)
        
        # ایجاد نمونه مهارت با نام و آیکون (در صورت وجود) و اختصاص به صنعت واکشی شده.
        skill = Skill.objects.create(
            name=validated_data.get('name'),
            icon=validated_data.get('icon'),
            industry=industry
        )
        # ذخیره مهارت (اگر تغییر خاصی نیاز باشد)
        skill.save()
        return skill

    def update(self, instance, validated_data):
        """
        به‌روزرسانی نمونه موجود مهارت.
        در صورتی که industry_slug در context موجود باشد، صنعت مربوطه به‌روزرسانی می‌شود.
        """
        # دریافت industry_slug از context؛ اگر موجود باشد، صنعت به‌روزرسانی می‌شود.
        industry_slug = self.context.get('industry_slug')
        if industry_slug:
            industry = get_object_or_404(Industry, slug=industry_slug)
            instance.industry = industry

        # به‌روزرسانی فیلد name؛ اگر داده جدید ارائه نشده باشد، مقدار قبلی حفظ می‌شود.
        instance.name = validated_data.get('name', instance.name)

        # در نهایت، ذخیره تغییرات
        instance.save()
        return instance
