from django.db import models  # ایمپورت مدل‌های Django جهت تعریف مدل‌های دیتابیس

# ایمپورت مدل‌های مرتبط از اپ‌های دیگر
from Companies.models import Company           # وارد کردن مدل Company از اپ Companies
from Industry.models import Industry             # وارد کردن مدل Industry از اپ Industry
from Locations.models import City                # وارد کردن مدل City از اپ Locations
from Users.models import User                    # وارد کردن مدل User از اپ Users
from Resumes.models import JobSeekerResume       # وارد کردن مدل JobSeekerResume از اپ Resumes
from Subscriptions.models import AdvertisementSubscription  # وارد کردن مدل AdvertisementSubscription از اپ Subscriptions

import uuid





class SalaryChoices(models.TextChoices):
    RANGE_5_TO_10 = '5 to 10', '5 تا 10 میلیون تومان'        # انتخاب محدوده حقوق از 5 تا 10 میلیون تومان
    RANGE_10_TO_15 = '10 to 15', '10 تا 15 میلیون تومان'      # انتخاب محدوده حقوق از 10 تا 15 میلیون تومان
    RANGE_15_TO_20 = '15 to 20', '15 تا 20 میلیون تومان'      # انتخاب محدوده حقوق از 15 تا 20 میلیون تومان
    RANGE_20_TO_30 = '20 to 30', '20 تا 30 میلیون تومان'      # انتخاب محدوده حقوق از 20 تا 30 میلیون تومان
    RANGE_30_TO_50 = '30 to 50', '30 تا 50 میلیون تومان'      # انتخاب محدوده حقوق از 30 تا 50 میلیون تومان
    MORE_THAN_50 = 'More than 50', 'بیش از 50 میلیون تومان'   # انتخاب محدوده حقوق بیش از 50 میلیون تومان
    NEGOTIABLE = 'Negotiable', 'توافقی'                        # انتخاب وضعیت توافقی برای حقوق

class GenderChoices(models.TextChoices):
    MALE = 'M', 'مرد'                 # انتخاب جنسیت مرد
    FEMALE = 'F', 'زن'               # انتخاب جنسیت زن
    NOT_SPECIFIED = 'N', 'مهم نیست'  # انتخاب حالت "مهم نیست"

class SoldierStatusChoices(models.TextChoices):
    COMPLETED = 'CO', 'پایان خدمت'                 # انتخاب وضعیت سربازی: پایان خدمت
    EDUCATIONAL_EXEMPTION = 'EE', 'معافیت تحصیلی'  # انتخاب معافیت تحصیلی
    NOT_SPECIFIED = 'NS', 'مهم نیست'            # انتخاب حالت "مهم نیست" برای سربازی

class DegreeChoices(models.TextChoices):
    BELOW_DIPLOMA = 'BD', 'زیر دیپلم'           # انتخاب حداقل مدرک زیر دیپلم
    DIPLOMA = 'DI', 'دیپلم'                             # انتخاب مدرک دیپلم
    ASSOCIATE = 'AS', 'فوق دیپلم'                    # انتخاب مدرک فوق دیپلم
    BACHELOR = 'BA', 'لیسانس'                         # انتخاب مدرک لیسانس
    MASTER = 'MA', 'فوق لیسانس'                         # انتخاب مدرک فوق لیسانس
    DOCTORATE = 'DO', 'دکترا'                         # انتخاب مدرک دکترا

class StatusChoices(models.TextChoices):
    PENDING = 'P', 'در حال بررسی'     # وضعیت آگهی: در حال بررسی
    APPROVED = 'A', 'تایید شده'         # وضعیت آگهی: تایید شده
    REJECTED = 'R', 'رد شده'            # وضعیت آگهی: رد شده


class JobTypeChoices(models.TextChoices):
    FULL_TIME = 'FT', 'تمام وقت'
    PART_TIME = 'PT', 'پاره وقت'
    REMOTE = 'RE', 'دورکاری'
    INTERNSHIP = 'IN', 'کارآموزی'




class Advertisement(models.Model):
    class TypeChoices(models.TextChoices):
        JOB = 'J', 'شغل'
        RESUME = 'R', 'رزومه'


    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)

    subscription = models.OneToOneField(
        AdvertisementSubscription,
        on_delete=models.CASCADE,
        related_name="advertisement",
        verbose_name="اشتراک"
    )

    ad_type = models.CharField(
        max_length=1,
        verbose_name="نوع آگهی",
        choices=TypeChoices.choices,
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")


class JobAdvertisement(models.Model):
    """
    مدل برای آگهی‌های کارفرما. این مدل اطلاعات بیشتری مانند شرکت و کارفرما را در بر می‌گیرد.
    """


    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)

    advertisement = models.OneToOneField(
        Advertisement,
        on_delete=models.CASCADE,
        verbose_name="آگهی",
        related_name="job_advertisement"
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="company_advertisements",
        verbose_name="شرکت"
    )

    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="employer_advertisements",
        verbose_name="کارفرما"
    )

    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        related_name="job_advertisements_industry",
        verbose_name="صنعت"
    )


    location = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="job_advertisements_location",
        verbose_name="موقعیت"
    )


    title = models.CharField(
        max_length=255, 
        verbose_name="عنوان آگهی"
    )

    description = models.TextField(
        verbose_name="توضیحات بیشتر",
        blank=True,
        null=True 
    )

    status = models.CharField(
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name="وضعیت آگهی"
    )

    gender = models.CharField(
        max_length=2,
        choices=GenderChoices.choices,
        verbose_name="جنسیت",
        blank=True, null=True
    )

    soldier_status = models.CharField(
        max_length=2,
        choices=SoldierStatusChoices.choices,
        verbose_name="وضعیت سربازی",
        blank=True, null=True
    )

    degree = models.CharField(
        max_length=2,
        choices=DegreeChoices.choices,
        verbose_name="حداقل مدرک تحصیلی",
        blank=True, null=True
    )

    salary = models.CharField(
        max_length=30,
        choices=SalaryChoices.choices,
        verbose_name="محدوده حقوق",
        blank=True, null=True
    )

    job_type = models.CharField(
        max_length=2,
        choices=JobTypeChoices.choices,
        verbose_name="نوع کار",
        blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "آگهی کارفرما"
        verbose_name_plural = "آگهی‌های کارفرما"

    def __str__(self):
        return f"{self.title} ({self.company.name})"



class ResumeAdvertisement(models.Model):
    """
    مدل برای آگهی‌های رزومه کارجو که آگهی‌های ارسال شده از سوی جویندگان کار را مدیریت می‌کند.
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)

    job_seeker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="resume_advertisements",
        verbose_name="پروفایل کارجو"
    )

    resume = models.ForeignKey(
        JobSeekerResume,
        on_delete=models.CASCADE,
        related_name="Resume",
        verbose_name="رزومه"
    )

    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        related_name="resume_advertisements_industry",
        verbose_name="صنعت"
    )


    advertisement = models.OneToOneField(
        Advertisement,
        on_delete=models.CASCADE,
        verbose_name="آگهی",
        related_name="resume_advertisement"
    )

    location = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="resume_advertisements_location",
        verbose_name="موقعیت"
    )


    title = models.CharField(
        max_length=255, 
        verbose_name="عنوان آگهی"
    )


    description = models.TextField(
        verbose_name="توضیحات بیشتر",
        blank=True,
        null=True 
    )

    status = models.CharField(
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name="وضعیت آگهی"
    )

    gender = models.CharField(
        max_length=2,
        choices=GenderChoices.choices,
        verbose_name="جنسیت",
        blank=True, null=True
    )

    soldier_status = models.CharField(
        max_length=2,
        choices=SoldierStatusChoices.choices,
        verbose_name="وضعیت سربازی",
        blank=True, null=True
    )

    degree = models.CharField(
        max_length=2,
        choices=DegreeChoices.choices,
        verbose_name="حداقل مدرک تحصیلی",
        blank=True, null=True
    )

    salary = models.CharField(
        max_length=30,
        choices=SalaryChoices.choices,
        default=SalaryChoices.NEGOTIABLE,
        verbose_name="محدوده حقوق",
        blank=True, null=True
    )

    job_type = models.CharField(
        max_length=2,
        choices=JobTypeChoices.choices,
        verbose_name="نوع کار",
        blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")


    class Meta:
        verbose_name = "آگهی رزومه کارجو"
        verbose_name_plural = "آگهی‌های رزومه کارجو"

    def __str__(self):
        return f"{self.title} ({self.job_seeker.username})"





class Application(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'PE', 'در انتظار'
        IN_REVIEW = 'IR', 'در حال بررسی'
        ACCEPTED = 'AC', 'پذیرفته شده'
        REJECTED = 'RE', 'رد شده'

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    
    job_seeker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    advertisement = models.ForeignKey(
        JobAdvertisement,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    
    cover_letter = models.TextField(blank=True)
    
    resume = models.ForeignKey(
        JobSeekerResume,
        on_delete=models.SET_NULL,
        null=True
    )
    
    status = models.CharField(
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    
    employer_notes = models.TextField(blank=True, null=True)
    viewed_by_employer = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.job_seeker.username} -> {self.advertisement.title}"
    
    def mark_as_viewed(self):
        """
        علامت‌گذاری درخواست به عنوان مشاهده شده توسط کارفرما.
        این متد، فیلد viewed_by_employer را به True تغییر می‌دهد و تغییرات را ذخیره می‌کند.
        """
        self.viewed_by_employer = True
        self.save() 
    
    def get_status_display_verbose(self):
        return self.get_status_display()
