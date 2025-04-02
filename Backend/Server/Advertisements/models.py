from django.db import models

from Companies.models import Company
from Industry.models import Industry
from Locations.models import City
from Users.models import User
from Profiles.models import JobSeekerProfile, EmployerProfile
from Resumes.models import JobSeekerResume
from Subscriptions.models import AdvertisementSubscription






class Advertisement(models.Model):
    """
    Abstract base model for common advertisement fields.
    """

    class SalaryChoices(models.TextChoices):
        RANGE_5_TO_10 = '5 to 10', '5 تا 10 میلیون تومان'
        RANGE_10_TO_15 = '10 to 15', '10 تا 15 میلیون تومان'
        RANGE_15_TO_20 = '15 to 20', '15 تا 20 میلیون تومان'
        RANGE_20_TO_30 = '20 to 30', '20 تا 30 میلیون تومان'
        RANGE_30_TO_50 = '30 to 50', '30 تا 50 میلیون تومان'
        MORE_THAN_50 = 'More than 50', 'بیش از 50 میلیون تومان'
        NEGOTIABLE = 'Negotiable', 'توافقی'

    class GenderChoices(models.TextChoices):
        MALE = 'Male', 'مرد'
        FEMALE = 'Female', 'زن'
        NOT_SPECIFIED = 'Not Specified', 'مهم نیست'

    class SoldierStatusChoices(models.TextChoices):
        COMPLETED = 'Completed', 'پایان خدمت'
        PERMANENT_EXEMPTION = 'Permanent Exemption', 'معافیت دائم'
        EDUCATIONAL_EXEMPTION = 'Educational Exemption', 'معافیت تحصیلی'
        NOT_SPECIFIED = 'Not Specified', 'مهم نیست'

    class DegreeChoices(models.TextChoices):
        BELOW_DIPLOMA = 'Below Diploma', 'زیر دیپلم'
        DIPLOMA = 'Diploma', 'دیپلم'
        ASSOCIATE = 'Associate', 'فوق دیپلم'
        BACHELOR = 'Bachelor', 'لیسانس'
        MASTER = 'Master', 'فوق لیسانس'
        DOCTORATE = 'Doctorate', 'دکترا'

    class StatusChoices(models.TextChoices):
        PENDING = 'Pending', 'در حال بررسی'
        APPROVED = 'Approved', 'تایید شده'
        REJECTED = 'Rejected', 'رد شده'

    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        related_name="Advertisements_Industry",
        verbose_name="صنعت"
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="Advertisement_Owner",
        verbose_name="مالک"
    )

    subscription = models.OneToOneField(
        AdvertisementSubscription,
        on_delete=models.CASCADE,
        related_name="Advertisements_Subscription",
        verbose_name="اشتراک"
    )

    location = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="Advertisements_Location",
        verbose_name="موقعیت"
    )

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان آگهی"
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="اسلاگ"
    )

    advertise_code = models.CharField(
        max_length=220,
        unique=True,
        db_index=True,
        verbose_name="کد آگهی",
        help_text="بعد از ثبت مقداردهی می‌شود"
    )

    description = models.TextField(
        verbose_name="توضیحات بیشتر",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name="وضعیت آگهی"
    )

    gender = models.CharField(
        max_length=20,
        choices=GenderChoices.choices,
        verbose_name="جنسیت"
    )

    soldier_status = models.CharField(
        max_length=30,
        choices=SoldierStatusChoices.choices,
        verbose_name="وضعیت سربازی"
    )

    degree = models.CharField(
        max_length=20,
        choices=DegreeChoices.choices,
        verbose_name="حداقل مدرک تحصیلی"
    )

    salary = models.CharField(
        max_length=20,
        choices=SalaryChoices.choices,
        default=SalaryChoices.NEGOTIABLE,
        verbose_name="محدوده حقوق"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class JobAdvertisement(models.Model):

    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        verbose_name="آگهی",
        related_name="Job_Advertisement"
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="Company_Advertisement",
        verbose_name="شرکت"
    )

    employer = models.ForeignKey(
        EmployerProfile,
        on_delete=models.CASCADE,
        related_name="Employer_Advertisement",
        verbose_name="کارفرما"
    )

    job_type = models.CharField(
        max_length=20,
        choices=[
            ('Full-Time', 'تمام وقت'),
            ('Part-Time', 'پاره وقت'),
            ('Remote', 'دورکاری'),
            ('Internship', 'کارآموزی')
        ],
        verbose_name="نوع کار"
    )

    description_position = models.TextField(
        verbose_name="موقعیت شغلی"
    )

    class Meta:
        verbose_name = "آگهی کارفرما"
        verbose_name_plural = "آگهی‌های کارفرما"

    def __str__(self):
        return f"{self.title} ({self.company.name})"


class ResumeAdvertisement(models.Model):

    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        verbose_name="آگهی",
        related_name="Resume_Advertisement"
    )

    job_seeker_profile = models.ForeignKey(
        JobSeekerProfile,
        on_delete=models.CASCADE,
        related_name="Profile",
        verbose_name="پروفایل کارجو"
    )

    resume = models.ForeignKey(
        JobSeekerResume,
        on_delete=models.CASCADE,
        related_name="Resume",
        verbose_name="رزومه"
    )

    job_type = models.CharField(
        max_length=20,
        choices=[
            ('Full-Time', 'تمام وقت'),
            ('Part-Time', 'پاره وقت'),
            ('Remote', 'دورکاری'),
            ('Internship', 'کارآموزی')
        ],
        verbose_name="نوع کار"
    )

    class Meta:
        verbose_name = "آگهی رزومه کارجو"
        verbose_name_plural = "آگهی‌های رزومه کارجو"

    def __str__(self):
        return f"{self.title} ({self.job_seeker_profile})"



class Application(models.Model):
    # TextChoices for status
    class StatusChoices(models.TextChoices):
        PENDING = 'PE', 'در انتظار'
        IN_REVIEW = 'IR', 'در حال بررسی'
        ACCEPTED = 'AC', 'پذیرفته شده'
        REJECTED = 'RE', 'رد شده'


    job_seeker = models.ForeignKey(
        JobSeekerProfile,
        on_delete=models.CASCADE,
        related_name="Applications"
    )

    advertisement = models.ForeignKey(
        JobAdvertisement,
        on_delete=models.CASCADE, 
        related_name="Applications"
    )

    cover_letter = models.TextField(blank=True)

    resume = models.ForeignKey(
        JobSeekerResume,
        on_delete=models.SET_NULL,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    employer_notes = models.TextField(blank=True, null=True)

    viewed_by_employer = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.job_seeker.user.username} -> {self.advertisement.title}"


    def mark_as_viewed(self):
        self.viewed_by_employer = True
        self.save()

    def get_status_display_verbose(self):
        return self.get_status_display()
