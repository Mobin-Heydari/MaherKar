from rest_framework import serializers  # وارد کردن کلاس‌های سریالایزر از Django REST framework

from .models import JobAdvertisement, Application, ResumeAdvertisement  
# ایمپورت مدل‌های مربوط به آگهی‌ها، آگهی‌های کارفرما، درخواست‌ها و آگهی‌های رزومه کارجو

from Companies.models import Company  # ایمپورت مدل Company از اپ شرکت‌ها
from Profiles.models import EmployerProfile, JobSeekerProfile  # ایمپورت مدل‌های پروفایل کارفرما و جوینده کار
from Resumes.models import JobSeekerResume  # ایمپورت مدل رزومه جوینده کار
# ایمپورت سریالایزرهای مورد استفاده برای نمایش اطلاعات مرتبط از اپ‌های مختلف:
from Companies.serializers import CompanySerializer  
from Industry.serializers import IndustrySerializer
from Locations.serializers import CitySerializer
from Subscriptions.serializers import AdvertisementSubscription  
from Profiles.serializers import JobSeekerProfileSerializer, EmployerProfileSerializer
from Resumes.serializers import JobSeekerResumeSerializer
from Users.serializers import UserSerializer

import uuid



# =================================================================
# سریالایزر JobAdvertisementSerializer برای مدل JobAdvertisement (آگهی کارفرما)
# =================================================================
class JobAdvertisementSerializer(serializers.ModelSerializer):
    # نمایش اطلاعات شرکت (Company) با استفاده از CompanySerializer
    company = CompanySerializer()
    # نمایش اطلاعات کارفرما (EmployerProfile) با استفاده از EmployerProfileSerializer
    employer = EmployerProfileSerializer()

    # فیلد ورودی جهت دریافت اسلاگ شرکت از کاربر (فقط برای نوشتن)
    company_id = serializers.CharField(write_only=True)
    # فیلد ورودی جهت دریافت اسلاگ کارفرما (فقط برای نوشتن)
    employer_id = serializers.CharField(write_only=True)

    class Meta:
        model = JobAdvertisement  # این سریالایزر مربوط به مدل JobAdvertisement است
        fields = [
            'id', 'advertisement', 'company_id', 'company',
            'employer', 'job_type', 'description_position'
        ]
        # برخی فیلدها به عنوان read-only تعریف شده‌اند تا توسط کاربر تغییر نکنند
        read_only_fields = ['id', 'company', 'employer']

    def create(self, validated_data):
        # گرفتن شیء request از context جهت دسترسی به اطلاعات کاربر
        request = self.context.get('request')

        # حذف فیلد company_id از داده‌های معتبر شده تا برای ایجاد عملیات جداگانه استفاده شود
        company_id = validated_data.pop("company_id")
        try:
            # تلاش برای واکشی شیء شرکت بر اساس اسلاگ دریافت شده
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            raise serializers.ValidationError({"company_id": "Company with the given id does not exist."})

        # ایجاد شی JobAdvertisement با استفاده از advertisement ایجاد شده، شرکت و کارفرمای واکشی‌شده و سایر داده‌ها
        job_advertisement = JobAdvertisement.objects.create(
            company=company,
            employer=company.employer,
            **validated_data
        )
        return job_advertisement

    def update(self, instance, validated_data):

        # به‌روزرسانی سایر فیلدهای JobAdvertisement که در validated_data موجودند
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()  # ذخیره تغییرات در دیتابیس
        return instance  # بازگرداندن شیء به‌روزرسانی‌شده


# =================================================================
# سریالایزر ResumeAdvertisementSerializer برای مدل ResumeAdvertisement (آگهی رزومه کارجو)
# =================================================================
class ResumeAdvertisementSerializer(serializers.ModelSerializer):
    # نمایش اطلاعات پروفایل جوینده کار با استفاده از JobSeekerProfileSerializer
    job_seeker_profile = JobSeekerProfileSerializer()
    # نمایش اطلاعات رزومه جوینده کار با استفاده از JobSeekerResumeSerializer
    resume = JobSeekerResumeSerializer()

    # فیلد ورودی جهت دریافت اسلاگ پروفایل جوینده (فقط نوشتنی)
    job_seeker_slug = serializers.CharField(write_only=True)
    # فیلد ورودی جهت دریافت اسلاگ رزومه (فقط نوشتنی)
    resume_slug = serializers.CharField(write_only=True)

    class Meta:
        model = ResumeAdvertisement  # این سریالایزر مربوط به مدل ResumeAdvertisement است
        fields = [
            'id', 'advertisement', 'resume_slug', 
            'job_seeker_profile', 'resume', 'job_type'
        ]
        # فیلدهایی که به صورت read-only تعریف شده‌اند؛ بنابراین کاربر نمی‌تواند آن‌ها را تغییر دهد
        read_only_fields = ['id', 'job_seeker_profile', 'resume', 'advertisement']

    def create(self, validated_data):
        # گرفتن شیء request از context جهت دسترسی به کاربر
        request = self.context.get('request')
        # گرفتن شناسه پروفایل جوینده از context (توسط ویو تنظیم شده)
        jobseeker_profile_id = self.context.get('jobseeker_profile_id')

        try:
            # تلاش برای واکشی پروفایل جوینده کار از مدل JobSeekerProfile
            job_seeker_profile = JobSeekerProfile.objects.get(id=jobseeker_profile_id)
        except JobSeekerProfile.DoesNotExist:
            raise serializers.ValidationError({"profile": "profile with the given id does not exist."})
        
        try:
            # تلاش برای واکشی رزومه مربوط به پروفایل جوینده کار
            resume = JobSeekerResume.objects.get(job_seeker_profile=job_seeker_profile)
        except JobSeekerProfile.DoesNotExist:
            raise serializers.ValidationError({"resume": "Resume with the given profile does not exist."})

        # ایجاد شی ResumeAdvertisement با استفاده از آگهی ایجاد شده، پروفایل جوینده، رزومه و سایر داده‌ها
        resume_advertisement = ResumeAdvertisement.objects.create(
            job_seeker_profile=job_seeker_profile,
            resume=resume,
            **validated_data
        )
        return resume_advertisement

    def update(self, instance, validated_data):
        # جلوگیری از به‌روزرسانی فیلدهای حساس مانند 'job_seeker_profile'، 'resume' و 'advertisement'
        forbidden_fields = ["job_seeker_profile", "resume", "advertisement"]
        for field in forbidden_fields:
            if field in validated_data:
                raise serializers.ValidationError({field: f"You cannot update the {field} field."})
        
        # به‌روزرسانی فیلدهای باقی‌مانده در instance بر اساس داده‌های ورودی
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()  # ذخیره تغییرات در دیتابیس

        return instance  # برگرداندن شیء به‌روزرسانی‌شده


# =================================================================
# سریالایزر ApplicationSerializer برای مدل Application (درخواست)
# =================================================================
class ApplicationSerializer(serializers.ModelSerializer):
    # نمایش اطلاعات جوینده کار به صورت nested با استفاده از JobSeekerProfileSerializer (غیر قابل تغییر)
    job_seeker = JobSeekerProfileSerializer(read_only=True)
    # نمایش اطلاعات رزومه جوینده برای درخواست با استفاده از JobSeekerResumeSerializer (غیر قابل تغییر)
    resume = JobSeekerResumeSerializer(read_only=True)

    # فیلدی برای نمایش وضعیت درخواست به صورت متنی؛ از متد get_status_display() استفاده می‌کند
    status_display = serializers.ReadOnlyField(source='get_status_display')

    class Meta:
        model = Application  # این سریالایزر مربوط به مدل Application است
        fields = [
            'id', 'job_seeker', 'advertisement', 'cover_letter', 'resume',
            'status', 'status_display', 'employer_notes', 'viewed_by_employer',
            'created_at', 'updated_at'
        ]
        # فیلدهایی که کاربر نمی‌تواند آن‌ها را تغییر دهد (فقط خواندنی)
        read_only_fields = [
            'id', 'job_seeker', 'advertisement', 'resume', 'status', 'status_display',
            'viewed_by_employer', 'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        # در زمان ایجاد درخواست، پروفایل جوینده به طور خودکار از کاربر احراز هویت شده گرفته می‌شود
        request = self.context.get("request")
        validated_data['job_seeker'] = request.user.profile  # فرض بر این است که JobSeekerProfile با User مرتبط است
        # فراخوانی متد create والد (برنامه‌نویسی استاندارد DRF) جهت ایجاد شیء Application
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        # تعریف لیستی از فیلدهای حساس که اجازه به تغییر آن‌ها داده نمی‌شود
        forbidden_fields = ["job_seeker", "advertisement", "resume"]

        # اگر کاربر درخواست به‌روزرسانی را ارسال می‌کند و مالک آگهی برابر با کاربر موجود در request است
        if request.user == instance.advertisement.advertisement.owner:
            # به‌روزرسانی وضعیت درخواست (به عنوان استثنا)
            instance.status = validated_data.get('status', instance.status)

        # بررسی اینکه هیچ یک از فیلدهای ممنوع به‌روزرسانی نشده باشد؛ در صورت وجود تغییر در این فیلدها، خطا صادر می‌شود
        for field in forbidden_fields:
            if field in validated_data:
                raise serializers.ValidationError({field: f"You cannot change the {field} field."})
        
        instance.save()  # ذخیره تغییرات اولیه
        # فراخوانی متد update والد جهت به‌روزرسانی سایر فیلدها
        return super().update(instance, validated_data)
