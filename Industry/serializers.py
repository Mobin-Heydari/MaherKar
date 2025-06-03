from django.shortcuts import get_object_or_404  # برای بازیابی شیء و ارسال خطای 404 در صورت عدم وجود
from rest_framework import serializers          # وارد کردن کتابخانه سریالایزرهای DRF
from .models import Industry, IndustryCategory, Skill  # ایمپورت مدل‌های مربوطه





class IndustryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryCategory  # مدل مرتبط: IndustryCategory
        fields = '__all__'

    def create(self, validated_data):
        """
        ایجاد یک نمونه جدید از دسته‌بندی.
        اسلاگ به صورت خودکار در متد save مدل تولید می‌شود.
        """
        category = IndustryCategory.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        """
        به‌روزرسانی نمونه‌ی موجود دسته‌بندی.
        """
        # به‌روزرسانی فیلد name؛ اگر مقدار جدید ارائه نشده باشد مقدار قبلی حفظ می‌شود.
        instance.name = validated_data.get('name', instance.name)

        instance.icon = validated_data.get('icon', instance.icon)
        # ذخیره تغییرات
        instance.save()
        return instance



class IndustrySerializer(serializers.ModelSerializer):
    # اضافه کردن فیلد category_id جهت نمایش نام دسته‌بندی مرتبط؛ خواندنی
    category_id = serializers.CharField(write_only=True, required=False)
    category = IndustryCategorySerializer(read_only=True)

    class Meta:
        model = Industry
        fields = [
            'id',
            'name',
            'icon',
            'category',
            'category_id'
        ]

    def create(self, validated_data):
        """
        ایجاد یک نمونه جدید از صنعت و اتصال آن به دسته‌بندی مرتبط.
        برای این کار، اسلاگ دسته‌بندی از context دریافت شده و دسته‌بندی مربوطه واکشی می‌شود.
        """
        # دریافت category_id از context؛ در صورتی که وجود نداشته باشد، اعتبارسنجی خطا خواهد داد.
        category_id = validated_data.pop('category_id', None)
        if not category_id:
            raise serializers.ValidationError({"category_id": "ID of the category is required."})
        
        # واکشی دسته‌بندی با استفاده از id
        category = get_object_or_404(IndustryCategory, id=category_id)

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
        # به‌روز‌رسانی آیکون صنعت یا نگهداری مقدار قبلی در صورت عدم ارائه مقدار جدید
        instance.icon = validated_data.get('icon', instance.icon)
        instance.save()
        return instance



class SkillSerializer(serializers.ModelSerializer):
    # نمایش جزئیات صنعت به‌عنوان فیلد تو در تو در نمایش مهارت؛ خواندنی است.
    industry = IndustrySerializer(read_only=True)
    industry_id = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Skill  # مدل مرتبط: Skill
        fields = ['id', 'name', 'icon', 'industry', 'industry_id']
    
    def create(self, validated_data):
        """
        ایجاد یک نمونه جدید از مهارت و اختصاص آن به یک صنعت.
        برای این منظور، industry_id از context دریافت شده و صنعت مربوطه واکشی می‌شود.
        """
        # دریافت industry_id از context؛ در صورت عدم وجود خطای اعتبارسنجی می‌دهد.
        industry_id = validated_data.pop('industry_id', None)
        if not industry_id:
            raise serializers.ValidationError({"industry_id": "ID of the industry is required."})
        
        try:
            industry = Industry.objects.get(id=industry_id)
        except:
            raise serializers.ValidationError({"industry_id": "The industry with this id not found."})
        
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
        industry_id = validated_data.pop('industry_id', None)
        if industry_id:
            try:
                industry = Industry.objects.get(id=industry_id)
            except:
                raise serializers.ValidationError({"industry_id": "The industry with this id not found."})
            instance.industry = industry
            instance.save()
        
        # به‌روزرسانی فیلد name؛ اگر داده جدید ارائه نشده باشد، مقدار قبلی حفظ می‌شود.
        instance.name = validated_data.get('name', instance.name)

        # در نهایت، ذخیره تغییرات
        instance.save()
        return instance
