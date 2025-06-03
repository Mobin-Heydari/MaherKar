from rest_framework import serializers  
# ایمپورت ماژول serializers از DRF برای مدیریت داده‌های ورودی و خروجی سریالایزرها

from .models import (
    ReportCategory,
    JobSeekerReport,
    EmployerReport,
)  
# ایمپورت مدل‌های مرتبط با اپ گزارش‌ها برای استفاده در سریالایزرها




# =============================================================================
# سریالایزر ReportCategorySerializer (دسته‌بندی گزارش‌ها)
# =============================================================================
class ReportCategorySerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل ReportCategory جهت مدیریت دسته‌بندی گزارش‌ها.
    """
    class Meta:
        model = ReportCategory  # اتصال سریالایزر به مدل ReportCategory
        fields = ['id', 'name', 'description']  
        # فیلدهایی که در خروجی سریالایزر نمایش داده می‌شوند: شناسه، نام و توضیحات دسته‌بندی


# =============================================================================
# سریالایزر JobSeekerReportSerializer (گزارش‌های جویندگان کار)
# =============================================================================
class JobSeekerReportSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل JobSeekerReport جهت مدیریت گزارش‌های مربوط به جویندگان کار.
    """
    # نمایش نام کاربری جوینده کار گزارش شده (فقط خواندنی)
    reported_jobseeker_username = serializers.ReadOnlyField(source='reported_jobseeker.user.username')
    # نمایش نام کاربری گزارش‌دهنده (فقط خواندنی)
    reporter_username = serializers.ReadOnlyField(source='reporter.username')

    class Meta:
        model = JobSeekerReport  # اتصال سریالایزر به مدل JobSeekerReport
        fields = [
            'id',  # شناسه گزارش
            'status',  # وضعیت گزارش
            'reported_jobseeker',  # جوینده کار گزارش شده
            'reported_jobseeker_username',  # نام کاربری جوینده کار گزارش شده
            'reporter',  # گزارش‌دهنده
            'reporter_username',  # نام کاربری گزارش‌دهنده
            'category',  # دسته‌بندی گزارش
            'description',  # توضیحات گزارش
            'created_at',  # زمان ایجاد گزارش
        ]

    def create(self, validated_data):
        """
        متد ایجاد یک گزارش جدید برای جویندگان کار.
        """
        return JobSeekerReport.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        متد به‌روزرسانی یک گزارش موجود.
        """
        # به‌روزرسانی وضعیت گزارش (اگر مقدار جدید وارد شده باشد)
        instance.status = validated_data.get('status', instance.status)
        # به‌روزرسانی توضیحات گزارش
        instance.description = validated_data.get('description', instance.description)
        instance.save()  # ذخیره تغییرات در دیتابیس
        return instance  # بازگرداندن نمونه به‌روزرسانی‌شده


# =============================================================================
# سریالایزر EmployerReportSerializer (گزارش‌های کارفرماها)
# =============================================================================
class EmployerReportSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل EmployerReport جهت مدیریت گزارش‌های مربوط به کارفرماها.
    """
    # نمایش نام کاربری کارفرمای گزارش شده (فقط خواندنی)
    reported_employer_username = serializers.ReadOnlyField(source='reported_employer.user.username')
    # نمایش نام کاربری گزارش‌دهنده (فقط خواندنی)
    reporter_username = serializers.ReadOnlyField(source='reporter.username')

    class Meta:
        model = EmployerReport  # اتصال سریالایزر به مدل EmployerReport
        fields = [
            'id',  # شناسه گزارش
            'status',  # وضعیت گزارش
            'reported_employer',  # کارفرمای گزارش شده
            'reported_employer_username',  # نام کاربری کارفرمای گزارش شده
            'reporter',  # گزارش‌دهنده
            'reporter_username',  # نام کاربری گزارش‌دهنده
            'category',  # دسته‌بندی گزارش
            'description',  # توضیحات گزارش
            'created_at',  # زمان ایجاد گزارش
        ]

    def create(self, validated_data):
        """
        متد ایجاد یک گزارش جدید برای کارفرماها.
        """
        return EmployerReport.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        متد به‌روزرسانی یک گزارش موجود.
        """
        # به‌روزرسانی وضعیت گزارش (اگر مقدار جدید وارد شده باشد)
        instance.status = validated_data.get('status', instance.status)
        # به‌روزرسانی توضیحات گزارش
        instance.description = validated_data.get('description', instance.description)
        instance.save()  # ذخیره تغییرات در دیتابیس
        return instance  # بازگرداندن نمونه به‌روزرسانی‌شده
