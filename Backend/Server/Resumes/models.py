from django.db import models  # وارد کردن ماژول models از Django جهت تعریف مدل‌های دیتابیس

# ایمپورت مدل‌های مرتبط از اپ‌های دیگر:
from Locations.models import City              # ایمپورت مدل City از اپ Locations جهت مدیریت اطلاعات مکان
from Industry.models import Industry, Skill      # ایمپورت مدل‌های Industry برای صنایع و Skill برای مهارت‌ها از اپ Industry




# ------------------------------
# مدل رزومه جوینده کار
# ------------------------------
class JobSeekerResume(models.Model):

    # تعریف گزینه‌های مربوط به حقوق مورد انتظار به صورت متنی
    class SalaryChoices(models.TextChoices):
        RANGE_5_TO_10 = '5 to 10', '5 تا 10 میلیون تومان'
        RANGE_10_TO_15 = '10 to 15', '10 تا 15 میلیون تومان'
        RANGE_15_TO_20 = '15 to 20', '15 تا 20 میلیون تومان'
        RANGE_20_TO_30 = '20 to 30', '20 تا 30 میلیون تومان'
        RANGE_30_TO_50 = '30 to 50', '30 تا 50 میلیون تومان'
        MORE_THAN_50 = 'More than 50', 'بیش از 50 میلیون تومان'
        NEGOTIABLE = 'Negotiable', 'توافقی'

    # تعریف گزینه‌های جنسیت رزومه
    class GenderChoices(models.TextChoices):
        MALE = 'Male', 'مرد'
        FEMALE = 'Female', 'زن'

    # تعریف گزینه‌های وضعیت سربازی
    class SoldierStatusChoices(models.TextChoices):
        COMPLETED = 'Completed', 'پایان خدمت'
        PERMANENT_EXEMPTION = 'Permanent Exemption', 'معافیت دائم'
        EDUCATIONAL_EXEMPTION = 'Educational Exemption', 'معافیت تحصیلی'
        NOT_COMPLETED = 'Not Completed', 'نااتمام'

    # تعریف گزینه‌های مدارک تحصیلی
    class DegreeChoices(models.TextChoices):
        BELOW_DIPLOMA = 'Below Diploma', 'زیر دیپلم'
        DIPLOMA = 'Diploma', 'دیپلم'
        ASSOCIATE = 'Associate', 'فوق دیپلم'
        BACHELOR = 'Bachelor', 'لیسانس'
        MASTER = 'Master', 'فوق لیسانس'
        DOCTORATE = 'Doctorate', 'دکترا'

    # تعریف گزینه‌های سابقه کاری (مدت همکاری)
    class CooperationTypeChoices(models.TextChoices):
        NO_EXPERIENCE = 'No EXPERIENCE', 'بدون سابقه کار'
        LESS_THAN_3_YEARS = 'Less than Three', 'کمتر از 3 سال'
        BETWEEN_3_AND_6_YEARS = 'Three or More', '3 تا 6 سال'
        MORE_THAN_6_YEARS = 'Six or More', 'بیشتر از 6 سال'

    # تعریف گزینه‌های نوع شغل مورد نظر
    class JobTypeChoices(models.TextChoices):
        FULL_TIME = 'Full-Time', 'تمام وقت'
        PART_TIME = 'Part-Time', 'پاره وقت'
        REMOTE = 'Remote', 'دورکاری'
        INTERNSHIP = 'Internship', 'کارآموزی'

    # تعریف گزینه‌های وضعیت دسترسی و موجودیت رزومه
    class AvailabilityChoices(models.TextChoices):
        IMMEDIATELY = 'immediately', 'فوری'
        WITH_NOTICE = 'with_notice', 'با اطلاع'
        NOT_AVAILABLE = 'not_available', 'غیرقابل دسترسی'

    # ارتباط یک به یک با پروفایل جوینده کار از اپ Profiles؛ هر رزومه متعلق به یک پروفایل جوینده کار است
    job_seeker_profile = models.OneToOneField(
        'Profiles.JobSeekerProfile',
        on_delete=models.CASCADE,
        related_name="Resume",
        verbose_name="جوینده کار"
    )

    # ارتباط به مدل Industry جهت تعیین صنعتی که رزومه مربوط به آن است
    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        verbose_name="صنعت",
        related_name="Resume_Industry"
    )

    # عنوان شغلی رزومه
    headline = models.CharField(
        max_length=255,
        verbose_name="عنوان شغلی"
    )

    # بیوگرافی یا توضیح مختصر درباره کاربر
    bio = models.TextField(
        blank=True,
        verbose_name="بیوگرافی"
    )

    # آدرس وب‌سایت شخصی یا حرفه‌ای
    website = models.URLField(
        blank=True,
        verbose_name="وب‌سایت"
    )

    # آدرس پروفایل لینکدین
    linkedin_profile = models.URLField(
        blank=True,
        verbose_name="لینکدین"
    )

    # ارتباط به مدل City جهت تعیین شهری که رزومه مربوط به آن است
    location = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="شهر"
    )

    # تعیین جنسیت رزومه بر اساس گزینه‌های تعریف شده
    gender = models.CharField(
        max_length=20,
        choices=GenderChoices.choices,
        verbose_name="جنسیت",
    )

    # تعیین وضعیت سربازی رزومه
    soldier_status = models.CharField(
        max_length=30,
        choices=SoldierStatusChoices.choices,
        verbose_name="وضعیت سربازی",
    )

    # تعیین مدرک تحصیلی رزومه
    degree = models.CharField(
        max_length=20,
        choices=DegreeChoices.choices,
        verbose_name="مدرک تحصیلی",
    )

    # تعداد سال سابقه مرتبط (به صورت عددی)
    years_of_experience = models.IntegerField(
        verbose_name="سال سابقه مرتبط",
        blank=True,
        null=True
    )

    # تعیین سابقه کاری به عنوان متن انتخابی از گزینه‌ها
    experience = models.CharField(
        max_length=50,
        choices=CooperationTypeChoices.choices,
        verbose_name="سابقه کاری",
    )

    # حقوق مورد انتظار با استفاده از گزینه‌های تعریف شده؛ مقدار پیش‌فرض 'توافقی'
    expected_salary = models.CharField(
        max_length=20,
        choices=SalaryChoices.choices,
        verbose_name="حقوق مورد نظر",
        default=SalaryChoices.NEGOTIABLE
    )

    # نوع شغل مورد علاقه کاربر (مثلاً تمام وقت یا پاره وقت)
    preferred_job_type = models.CharField(
        max_length=20,
        choices=JobTypeChoices.choices,
        verbose_name="نوع شغل مورد علاقه"
    )

    # فیلد بارگذاری فایل رزومه (CV)؛ فایل‌ها در مسیر مشخص ذخیره می‌شوند
    cv = models.FileField(
        upload_to='jobseekers/resumes/',
        verbose_name="رزومه"
    )

    # وضعیت دسترسی رزومه (مثلاً فوری یا با اطلاع)
    availability = models.CharField(
        max_length=20,
        choices=AvailabilityChoices.choices,
        verbose_name="وضعیت دسترسی",
        default=AvailabilityChoices.IMMEDIATELY
    )

    # تاریخ و زمان ایجاد رزومه؛ به صورت خودکار ثبت می‌شود
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )

    # تاریخ و زمان به‌روزرسانی رزومه؛ در هر تغییر به‌روز می‌شود
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی",
    )


# ------------------------------
# مدل تجربه کاری رزومه (Experience)
# ------------------------------
class Experience(models.Model):

    # تعریف گزینه‌های نوع قرارداد یا استخدامی برای تجربه کاری
    class EmploymentTypeChoices(models.TextChoices):
        FULL_TIME = 'full_time', 'تمام وقت'
        PART_TIME = 'part_time', 'پاره وقت'
        CONTRACTUAL = 'contractual', 'قراردادی'

    # ارتباط به مدل JobSeekerResume؛ هر تجربه به یک رزومه جوینده کار مربوط است
    resume = models.ForeignKey(
        JobSeekerResume,
        on_delete=models.CASCADE,
        verbose_name="رزومه",
        related_name="Experiences"
    )

    # نوع استخدام (تمام وقت، پاره وقت و یا قراردادی)
    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentTypeChoices.choices,
        verbose_name="نوع استخدام",
    )

    # عنوان شغلی یا نقش انجام شده در تجربه کاری
    title = models.CharField(
        max_length=255,
        verbose_name="عنوان شغلی",
        help_text="عنوان شغلی یا نقش در این تجربه"
    )

    # نام شرکت یا سازمان مربوط به تجربه کاری
    company = models.CharField(
        max_length=255,
        verbose_name="شرکت"
    )

    # ارتباط به مدل City جهت تعیین محل شرکت؛ استفاده از related_name جهت دسترسی راحت‌تر به مکان شرکت‌ها
    location = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="company_locations",
        verbose_name="مکان"
    )

    # تاریخ شروع تجربه کاری
    start_date = models.DateField(
        verbose_name="تاریخ شروع"
    )

    # تاریخ پایان تجربه کاری؛ این فیلد اختیاری و می‌تواند تهی باشد
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ پایان"
    )

    # توضیحات تکمیلی درباره تجربه کاری
    description = models.TextField(
        blank=True,
        verbose_name="توضیحات"
    )

    class Meta:
        verbose_name = "تجربه کاری"
        verbose_name_plural = "تجربیات کاری"
        ordering = ['-start_date']  # ترتیب نزولی بر اساس تاریخ شروع

    def __str__(self):
        return f"{self.title} at {self.company}"  # نمایش عنوان شغلی به همراه نام شرکت


# ------------------------------
# مدل تحصیلات (Education)
# ------------------------------
class Education(models.Model):

    # تعریف گزینه‌های مدارک تحصیلی مربوط به تحصیلات
    class DegreeChoices(models.TextChoices):
        DIPLOMA = 'Diploma', 'دیپلم'
        ASSOCIATE = 'Associate', 'فوق دیپلم'
        BACHELOR = 'Bachelor', 'لیسانس'
        MASTER = 'Master', 'فوق لیسانس'
        DOCTORATE = 'Doctorate', 'دکترا'

    # ارتباط به مدل JobSeekerResume؛ هر تحصیلات به یک رزومه جوینده کار مربوط است
    resume = models.ForeignKey(
        JobSeekerResume,
        on_delete=models.CASCADE,
        verbose_name="رزومه",
        related_name="Educations"
    )

    # نام مدرسه یا دانشگاه
    school = models.CharField(
        max_length=255,
        verbose_name="دانشگاه/مدرسه"
    )

    # مدرک تحصیلی دریافت شده
    degree = models.CharField(
        max_length=30,
        choices=DegreeChoices.choices,
        verbose_name="مدرک تحصیلی"
    )

    # نمره یا معدل تحصیلی؛ اختیاری
    grade = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="نمره یا معدل"
    )

    # رشته یا گرایش تحصیلی
    field_of_study = models.CharField(
        max_length=255,
        verbose_name="رشته تحصیلی"
    )

    # تاریخ شروع تحصیلات
    start_date = models.DateField(
        verbose_name="تاریخ شروع"
    )

    # تاریخ پایان تحصیلات؛ اختیاری
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ پایان"
    )
    
    # توضیحات تکمیلی درباره تحصیلات
    description = models.TextField(
        blank=True,
        verbose_name="توضیحات"
    )

    class Meta:
        verbose_name = "تحصیلات"
        verbose_name_plural = "تحصیلات"
        ordering = ['-start_date']  # ترتیب نزولی بر اساس تاریخ شروع

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} at {self.school}"  # نمایش مدرک به همراه رشته و نام نهاد آموزشی


# ------------------------------
# مدل مهارت‌های رزومه جوینده کار
# ------------------------------
class JobSeekerSkill(models.Model):
    # تعریف گزینه‌های سطح مهارت
    class LevelChoices(models.TextChoices):
        BEGINNER = 'beginner', 'مبتدی'
        INTERMEDIATE = 'intermediate', 'متوسط'
        ADVANCED = 'advanced', 'پیشرفته'
        EXPERT = 'expert', 'حرفه‌ای'

    # ارتباط به مدل JobSeekerResume؛ هر مهارت به یک رزومه جوینده کار مربوط است
    resume = models.ForeignKey(
        JobSeekerResume,
        on_delete=models.CASCADE,
        verbose_name="رزومه",
        related_name="Job_Seeker_Skills"
    )

    # ارتباط به مدل Skill جهت انتخاب مهارت از لیست مهارت‌های تعریف شده
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name="مهارت",
        related_name="Job_Seeker"
    )

    # تعیین سطح مهارت با استفاده از گزینه‌های تعریف شده
    level = models.CharField(
        max_length=20,
        choices=LevelChoices.choices,
        verbose_name="سطح مهارت"
    )

    def __str__(self):
        # نمایش نام مهارت به همراه سطح آن (استفاده از متد get_level_display جهت نمایش مقدار خوانا)
        return f"{self.skill.name} ({self.get_level_display()})"
