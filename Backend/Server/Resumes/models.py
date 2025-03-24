from django.db import models

from Locations.models import City
from Industry.models import Industry, Skill





class JobSeekerResume(models.Model):

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

    class SoldierStatusChoices(models.TextChoices):
        COMPLETED = 'Completed', 'پایان خدمت'
        PERMANENT_EXEMPTION = 'Permanent Exemption', 'معافیت دائم'
        EDUCATIONAL_EXEMPTION = 'Educational Exemption', 'معافیت تحصیلی'
        NOT_COMPLETED = 'Not Completed', 'نااتمام'

    class DegreeChoices(models.TextChoices):
        BELOW_DIPLOMA = 'Below Diploma', 'زیر دیپلم'
        DIPLOMA = 'Diploma', 'دیپلم'
        ASSOCIATE = 'Associate', 'فوق دیپلم'
        BACHELOR = 'Bachelor', 'لیسانس'
        MASTER = 'Master', 'فوق لیسانس'
        DOCTORATE = 'Doctorate', 'دکترا'

    class CooperationTypeChoices(models.TextChoices):
        NO_EXPERIENCE = 'No EXPERIENCE', 'بدون سابقه کار'
        LESS_THAN_3_YEARS = 'Less than Three', 'کمتر از 3 سال'
        BETWEEN_3_AND_6_YEARS = 'Three or More', '3 تا 6 سال'
        MORE_THAN_6_YEARS = 'Six or More', 'بیشتر از 6 سال'

    class JobTypeChoices(models.TextChoices):
        FULL_TIME = 'Full-Time', 'تمام وقت'
        PART_TIME = 'Part-Time', 'پاره وقت'
        REMOTE = 'Remote', 'دورکاری'
        INTERNSHIP = 'Internship', 'کارآموزی'

    class AvailabilityChoices(models.TextChoices):
        IMMEDIATELY = 'immediately', 'فوری'
        WITH_NOTICE = 'with_notice', 'با اطلاع'
        NOT_AVAILABLE = 'not_available', 'غیرقابل دسترسی'



    job_seeker_profile = models.OneToOneField(
        'Profiles.JobSeekerProfile',
        on_delete=models.CASCADE,
        related_name="Resume",
        verbose_name="جوینده کار"
    )

    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        verbose_name="صنعت",
        related_name="Resume_Industry"
    )


    headline = models.CharField(
        max_length=255,
        verbose_name="عنوان شغلی"
    )

    bio = models.TextField(
        blank=True,
        verbose_name="بیوگرافی"
    )

    website = models.URLField(
        blank=True,
        verbose_name="وب‌سایت"
    )

    linkedin_profile = models.URLField(
        blank=True,
        verbose_name="لینکدین"
    )

    location = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="شهر"
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
        verbose_name="مدرک تحصیلی",
    )

    years_of_experience = models.IntegerField(
        verbose_name="سال سابقه مرتبط",
        blank=True,
        null=True
    )

    experience = models.CharField(
        max_length=50,
        choices=CooperationTypeChoices.choices,
        verbose_name="سابقه کاری",
    )

    expected_salary = models.CharField(
        max_length=20,
        choices=SalaryChoices.choices,
        verbose_name="حقوق مورد نظر",
        default=SalaryChoices.NEGOTIABLE
    )

    preferred_job_type = models.CharField(
        max_length=20,
        choices=JobTypeChoices.choices,
        verbose_name="نوع شغل مورد علاقه"
    )

    cv = models.FileField(
        upload_to='jobseekers/resumes/',
        verbose_name="رزومه"
    )

    availability = models.CharField(
        max_length=20,
        choices=AvailabilityChoices.choices,
        verbose_name="وضعیت دسترسی",
        default=AvailabilityChoices.IMMEDIATELY
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی",
    )


class Experience(models.Model):

    class EmploymentTypeChoices(models.TextChoices):
        FULL_TIME = 'full_time', 'تمام وقت'
        PART_TIME = 'part_time', 'پاره وقت'
        CONTRACTUAL = 'contractual', 'قراردادی'


    resume = models.ForeignKey(
        JobSeekerResume,
        on_delete=models.CASCADE,
        verbose_name="رزومه",
        related_name="Experiences"
    )

    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentTypeChoices.choices,
        verbose_name="نوع استخدام",
    )


    title = models.CharField(
        max_length=255,
        verbose_name="عنوان شغلی",
        help_text="عنوان شغلی یا نقش در این تجربه"
    )

    company = models.CharField(
        max_length=255,
        verbose_name="شرکت"
    )

    location = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="company_locations",
        verbose_name="مکان"
    )

    start_date = models.DateField(
        verbose_name="تاریخ شروع"
    )

    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ پایان"
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات"
    )

    class Meta:
        verbose_name = "تجربه کاری"
        verbose_name_plural = "تجربیات کاری"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} at {self.company}"


class Education(models.Model):

    class DegreeChoices(models.TextChoices):
        DIPLOMA = 'Diploma', 'دیپلم'
        ASSOCIATE = 'Associate', 'فوق دیپلم'
        BACHELOR = 'Bachelor', 'لیسانس'
        MASTER = 'Master', 'فوق لیسانس'
        DOCTORATE = 'Doctorate', 'دکترا'
    

    resume = models.ForeignKey(
        JobSeekerResume,
        on_delete=models.CASCADE,
        verbose_name="رزومه",
        related_name="Educations"
    )

    school = models.CharField(
        max_length=255,
        verbose_name="دانشگاه/مدرسه"
    )

    degree = models.CharField(
        max_length=30,
        choices=DegreeChoices.choices,
        verbose_name="مدرک تحصیلی"
    )

    grade = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="نمره یا معدل"
    )


    field_of_study = models.CharField(
        max_length=255,
        verbose_name="رشته تحصیلی"
    )

    start_date = models.DateField(
        verbose_name="تاریخ شروع"
    )

    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ پایان"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="توضیحات"
    )

    class Meta:
        verbose_name = "تحصیلات"
        verbose_name_plural = "تحصیلات"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} at {self.school}"


class JobSeekerSkill(models.Model):
    class LevelChoices(models.TextChoices):
        BEGINNER = 'beginner', 'مبتدی'
        INTERMEDIATE = 'intermediate', 'متوسط'
        ADVANCED = 'advanced', 'پیشرفته'
        EXPERT = 'expert', 'حرفه‌ای'

    resume = models.ForeignKey(
        JobSeekerResume,
        on_delete=models.CASCADE,
        verbose_name="رزومه",
        related_name="Job_Seeker_Skills"
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name="مهارت",
        related_name="Job_Seeker"
    )

    level = models.CharField(
        max_length=20,
        choices=LevelChoices.choices,
        verbose_name="سطح مهارت"
    )

    def __str__(self):
        return f"{self.skill.name} ({self.get_level_display()})"