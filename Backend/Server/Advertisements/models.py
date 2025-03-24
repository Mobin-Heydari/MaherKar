from django.db import models


from Companies.models import Company
from Users.models import User
from Industry.models import Industry
from Locations.models import City
from Profiles.models import JobSeekerProfile
from Resumes.models import JobSeekerResume




class JobAdvertisement(models.Model):

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
        NOT_SPECIFIED = 'Not Specified', 'مهم نیست'
        BELOW_DIPLOMA = 'Below Diploma', 'زیر دیپلم'
        DIPLOMA = 'Diploma', 'دیپلم'
        ASSOCIATE = 'Associate', 'فوق دیپلم'
        BACHELOR = 'Bachelor', 'لیسانس'
        MASTER = 'Master', 'فوق لیسانس'
        DOCTORATE = 'Doctorate', 'دکترا'

    class CooperationTypeChoices(models.TextChoices):
        NOT_SPECIFIED = 'Does Not Matter', 'مهم نیست'
        LESS_THAN_3_YEARS = 'Less than Three', 'کمتر از 3 سال'
        BETWEEN_3_AND_6_YEARS = 'Three or More', '3 تا 6 سال'
        MORE_THAN_6_YEARS = 'Six or More', 'بیشتر از 6 سال'

    class JobTypeChoices(models.TextChoices):
        FULL_TIME = 'Full-Time', 'تمام وقت'
        PART_TIME = 'Part-Time', 'پاره وقت'
        REMOTE = 'Remote', 'دورکاری'
        INTERNSHIP = 'Internship', 'کارآموزی'

    class StatusChoices(models.TextChoices):
        PENDING = 'Pending', 'در حال بررسی'
        APPROVED = 'Approved', 'تایید شده'
        REJECTED = 'Rejected', 'رد شده'



    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="advertisements",
    )

    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        related_name="advertisements",
    )

    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="advertisements",
    )

    location = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="advertisements",
    )

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان آگهی",
    )
    
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="اسلاگ",
    )

    advertise_code = models.CharField(
        max_length=220,
        unique=True,
        db_index=True,
        verbose_name="کد آگهی",
        help_text="بعد از ثبت مقداردهی می‌شود",
    )

    description_position = models.TextField(
        verbose_name="موقعیت شغلی",
    )

    status = models.CharField(
        max_length=20,
        verbose_name="وضعیت آکهی",
        default=StatusChoices.PENDING
    )

    gender = models.CharField(
        max_length=20,
        choices=GenderChoices.choices,
        verbose_name="جنسیت",
    )

    soldier_status = models.CharField(
        max_length=30,
        choices=SoldierStatusChoices.choices,
        verbose_name="وضعیت سربازی",
    )

    degree = models.CharField(
        max_length=20,
        choices=DegreeChoices.choices,
        verbose_name="حداقل مدرک تحصیلی",
    )

    experience = models.CharField(
        max_length=50,
        choices=CooperationTypeChoices.choices,
        verbose_name="حداقل سابقه کاری",
    )

    salary = models.CharField(
        max_length=20,
        choices=SalaryChoices.choices,
        verbose_name="محدوده حقوق",
        default=SalaryChoices.NEGOTIABLE
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی",
    )

    def __str__(self):
        return f"{self.slug} - {self.company.name}"

    class Meta:
        verbose_name = "آگهی کارفرما"
        verbose_name_plural = "آگهی کارفرمایان"
        ordering = ["-created_at"]





class Application(models.Model):
    # TextChoices for status
    class StatusChoices(models.TextChoices):
        PENDING = 'PE', 'در انتظار'
        IN_REVIEW = 'IR', 'در حال بررسی'
        ACCEPTED = 'AC', 'پذیرفته شده'
        REJECTED = 'RE', 'رد شده'


    job_seeker = models.ForeignKey(
        'Profiles.JobSeekerProfile',
        on_delete=models.CASCADE,
        related_name="applications"
    )

    advertisement = models.ForeignKey(
        'Advertisements.JobAdvertisement',
        on_delete=models.CASCADE, 
        related_name="applications"
    )

    cover_letter = models.TextField(blank=True)

    resume = models.ForeignKey(
        'Resumes.JobSeekerResume',
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
