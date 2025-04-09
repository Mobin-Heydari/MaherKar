from rest_framework import serializers  # وارد کردن کلاس‌های سریالایزر از Django REST framework

from .models import Advertisement, JobAdvertisement, Application, ResumeAdvertisement  
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




# =================================================================
# سریالایزر AdvertisementSerializer برای مدل Advertisement (آگهی عمومی)
# =================================================================
class AdvertisementSerializer(serializers.ModelSerializer):
    # نمایش اطلاعات مالک آگهی با استفاده از سریالایزر کاربر
    owner = UserSerializer()
    # نمایش اطلاعات صنعت مربوط به آگهی
    industry = IndustrySerializer()
    # نمایش اطلاعات موقعیت (شهر) مربوط به آگهی
    location = CitySerializer()
    # نمایش اطلاعات اشتراک آگهی (Subscription) با سریالایزر مربوطه
    subscription = AdvertisementSubscription()

    # فیلد ورودی جهت دریافت اسلاگ صنعت از کاربر (write-only به صورت پیش‌فرض نیست مگر اینکه استفاده شود)
    industry_slug = serializers.CharField()
    # فیلد ورودی جهت دریافت اسلاگ موقعیت (شهر)
    location_slug = serializers.CharField()

    class Meta:
        model = Advertisement  # این سریالایزر مربوط به مدل Advertisement است
        fields = [
            'id', 'owner', 'industry', 'subscription', 'location', 'title', 'slug',
            'advertise_code', 'description', 'status', 'gender',
            'soldier_status', 'degree', 'salary', 'created_at', 'updated_at'
        ]
        # فیلدهایی که فقط برای خواندن در نظر گرفته شده‌اند، یعنی کاربر نمی‌تواند آن‌ها را تغییر دهد
        read_only_fields = ['id', 'advertise_code', 'slug', 'created_at', 'updated_at', 'subscription', 'owner']
    
    def update(self, instance, validated_data):
        # گرفتن شیء request از context جهت دسترسی به کاربر
        request = self.context.get('request')
        
        # اگر کاربر دارای مجوز admin باشد، اجازه به‌روزرسانی وضعیت آگهی را دارد
        if request.user.is_staff:
            instance.status = validated_data.get("status", instance.status)
        
        # به‌روزرسانی سایر فیلدهای موجود در validated_data به شیء instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()  # ذخیره تغییرات در دیتابیس
        return instance  # برگرداندن شیء به‌روزرسانی‌شده


# =================================================================
# سریالایزر JobAdvertisementSerializer برای مدل JobAdvertisement (آگهی کارفرما)
# =================================================================
class JobAdvertisementSerializer(serializers.ModelSerializer):
    # نمایش اطلاعات سطح تو در تو از Advertisement با استفاده از AdvertisementSerializer
    advertisement = AdvertisementSerializer()
    # نمایش اطلاعات شرکت (Company) با استفاده از CompanySerializer
    company = CompanySerializer()
    # نمایش اطلاعات کارفرما (EmployerProfile) با استفاده از EmployerProfileSerializer
    employer = EmployerProfileSerializer()

    # فیلد ورودی جهت دریافت اسلاگ شرکت از کاربر (فقط برای نوشتن)
    company_slug = serializers.CharField(write_only=True)
    # فیلد ورودی جهت دریافت اسلاگ کارفرما (فقط برای نوشتن)
    employer_slug = serializers.CharField(write_only=True)

    class Meta:
        model = JobAdvertisement  # این سریالایزر مربوط به مدل JobAdvertisement است
        fields = [
            'id', 'advertisement', 'company_slug', 'company',
            'employer', 'job_type', 'description_position'
        ]
        # برخی فیلدها به عنوان read-only تعریف شده‌اند تا توسط کاربر تغییر نکنند
        read_only_fields = ['id', 'company', 'employer']

    def create(self, validated_data):
        # گرفتن شیء request از context جهت دسترسی به اطلاعات کاربر
        request = self.context.get('request')
        # گرفتن شناسه کارفرما از context (توسط ویو تنظیم شده)
        employer_profile_id = self.context.get("employer_profile_id")

        # حذف فیلد company_slug از داده‌های معتبر شده تا برای ایجاد عملیات جداگانه استفاده شود
        company_slug = validated_data.pop("company_slug")
        try:
            # تلاش برای واکشی شیء شرکت بر اساس اسلاگ دریافت شده
            company = Company.objects.get(slug=company_slug)
        except Company.DoesNotExist:
            raise serializers.ValidationError({"company_slug": "Company with the given slug does not exist."})

        try:
            # تلاش برای واکشی پروفایل کارفرما بر اساس employer_profile_id
            employer = EmployerProfile.objects.get(id=employer_profile_id)
        except Company.DoesNotExist:
            # در صورتی که پروفایل کارفرما وجود نداشته باشد، خطای مربوطه صادر می‌شود
            raise serializers.ValidationError({"employer": "Employer profile with the given id does not exist."})

        # حذف داده‌های مربوط به advertisement (آگهی عمومی) از داده‌های ورودی
        advertisement_data = validated_data.pop("advertisement")
        # ایجاد یک شی Advertisement با مالک request.user و سایر داده‌های موجود
        advertisement = Advertisement.objects.create(
            owner=request.user,
            **advertisement_data
        )

        # ایجاد شی JobAdvertisement با استفاده از advertisement ایجاد شده، شرکت و کارفرمای واکشی‌شده و سایر داده‌ها
        job_advertisement = JobAdvertisement.objects.create(
            advertisement=advertisement,
            company=company,
            employer=employer,
            **validated_data
        )
        return job_advertisement

    def update(self, instance, validated_data):
        # جلوگیری از به‌روزرسانی فیلدهای حساس "company" و "employer"
        forbidden_fields = ["company", "employer"]
        for field in forbidden_fields:
            if field in validated_data:
                raise serializers.ValidationError({field: f"You cannot update the {field} field."})

        # به‌روزرسانی سایر فیلدهای JobAdvertisement که در validated_data موجودند
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()  # ذخیره تغییرات در دیتابیس
        return instance  # بازگرداندن شیء به‌روزرسانی‌شده


# =================================================================
# سریالایزر ResumeAdvertisementSerializer برای مدل ResumeAdvertisement (آگهی رزومه کارجو)
# =================================================================
class ResumeAdvertisementSerializer(serializers.ModelSerializer):
    # نمایش اطلاعات آگهی عمومی با استفاده از AdvertisementSerializer
    advertisement = AdvertisementSerializer()
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

        # حذف داده‌های مربوط به آگهی عمومی از validated_data
        advertisement_data = validated_data.pop("advertisement")
        # ایجاد شی Advertisement با مالک request.user و دیگر داده‌های مربوط به آگهی
        advertisement = Advertisement.objects.create(
            owner=request.user,
            **advertisement_data
        )

        # ایجاد شی ResumeAdvertisement با استفاده از آگهی ایجاد شده، پروفایل جوینده، رزومه و سایر داده‌ها
        resume_advertisement = ResumeAdvertisement.objects.create(
            advertisement=advertisement,
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
