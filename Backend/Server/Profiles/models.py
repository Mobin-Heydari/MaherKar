from django.db import models
from django.utils.text import slugify

from Locations.models import City




class PersonalInformation(models.Model):
    class Gender(models.TextChoices):
        WOMEN = 'W', 'خانوم'
        MAN = 'M', 'آقا'

    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        verbose_name="جنسیت",
        default=Gender.MAN
    )
    age = models.PositiveIntegerField(
        verbose_name="سن",
        default=18
    )

    class Meta:
        verbose_name = "اطلاعات شخصی"
        verbose_name_plural = "اطلاعات شخصی"

    def __str__(self):
        return f"{self.get_gender_display()} - {self.age}"


class IdCardInformation(models.Model):
    class IdCardStatus(models.TextChoices):
        PENDING = 'P', 'در انتظار تایید'
        VERIFIED = 'V', 'تایید شده'
        REJECTED = 'R', 'رد شده'

    id_card_number = models.CharField(
        verbose_name="شماره ملی",
        max_length=13,
        blank=True,
        null=True,
    )
    id_card = models.FileField(
        upload_to='jobseekers/id_cards/',
        verbose_name="کارت ملی",
        help_text="بارگذاری تصویر/اسکن کارت ملی",
        blank=True,
        null=True,
    )
    id_card_status = models.CharField(
        max_length=1,
        choices=IdCardStatus.choices,
        default=IdCardStatus.PENDING,
        verbose_name="وضعیت کارت ملی",
        help_text="وضعیت بررسی کارت ملی"
    )

    class Meta:
        verbose_name = "اطلاعات کارت ملی"
        verbose_name_plural = "اطلاعات کارت ملی"

    def __str__(self):
        id_val = self.id_card_number if self.id_card_number else "No ID"
        return f"{id_val} - {self.get_id_card_status_display()}"




class JobSeekerProfile(models.Model):
    """
    پروفایل جوینده کار به سبک لینکدین.
    شامل اطلاعات حرفه‌ای و شخصی برای جویندگان کار.
    """
    user = models.OneToOneField(
        "Users.User",
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    personal_info = models.OneToOneField(
        PersonalInformation,
        on_delete=models.CASCADE,
        verbose_name="اطلاعات شخصی",
        related_name="jobseeker_personal_info"
    )
    id_card_info = models.OneToOneField(
        IdCardInformation,
        on_delete=models.CASCADE,
        verbose_name="اطلاعات کارت ملی",
        related_name="jobseeker_id_card_info"
    )
    kids_count = models.PositiveIntegerField(
        default=0,
        verbose_name="تعداد فرزند"
    )
    headline = models.CharField(
        max_length=255,
        verbose_name="عنوان شغلی",
        help_text="عنوان شغلی کوتاه (الزامی)"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="بیوگرافی",
        help_text="توضیح مختصر درباره خودتان"
    )
    profile_picture = models.ImageField(
        upload_to='jobseekers/profile_pics/',
        null=True,
        blank=True,
        verbose_name="تصویر پروفایل"
    )
    location = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="شهر"
    )
    industry = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="صنعت",
        help_text="حوزه فعالیت شغلی"
    )
    contact_email = models.EmailField(
        blank=True,
        verbose_name="ایمیل تماس"
    )
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="شماره تماس"
    )
    website = models.URLField(
        blank=True,
        verbose_name="وب‌سایت"
    )
    linkedin_profile = models.URLField(
        blank=True,
        verbose_name="لینکدین"
    )
    resume = models.FileField(
        upload_to='jobseekers/resumes/',
        verbose_name="رزومه",
        help_text="بارگذاری فایل رزومه (CV)"
    )
    job_type_preference = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="نوع شغل مورد نظر",
        help_text="مثلاً تمام‌وقت یا پاره‌وقت"
    )
    expected_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="حقوق مورد انتظار"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    class Meta:
        verbose_name = "پروفایل جوینده کار"
        verbose_name_plural = "پروفایل‌های جویندگان کار"

    def __str__(self):
        return f"{self.user.username} - پروفایل جوینده کار"


class Experience(models.Model):
    """
    مدل تجربه کاری برای جویندگان کار.
    مشابه بخش تجربه‌های کاری لینکدین.
    """
    job_seeker = models.ForeignKey(
        JobSeekerProfile,
        on_delete=models.CASCADE,
        related_name="experiences",
        verbose_name="جوینده کار"
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
    """
    مدل تحصیلات، مشابه بخش تحصیلات لینکدین.
    """
    job_seeker = models.ForeignKey(
        JobSeekerProfile,
        on_delete=models.CASCADE,
        related_name="educations",
        verbose_name="جوینده کار"
    )
    school = models.CharField(
        max_length=255,
        verbose_name="دانشگاه/مدرسه"
    )
    degree = models.CharField(
        max_length=255,
        verbose_name="مدرک تحصیلی"
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


class SkillCategory(models.Model):
    """
    مدل دسته‌بندی مهارت‌ها.
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="نام دسته",
        help_text="نام دسته‌بندی مهارت (مثلاً 'برنامه نویسی' یا 'طراحی')"
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="اسلاگ دسته",
        help_text="اسلاگ برای دسته‌بندی که معمولاً از نام تولید می‌شود"
    )
    icon = models.ImageField(
        upload_to='skill_category_icons/',
        null=True,
        blank=True,
        verbose_name="آیکون دسته",
        help_text="تصویر یا آیکون مرتبط با دسته‌بندی (اختیاری)"
    )

    class Meta:
        verbose_name = "دسته مهارت"
        verbose_name_plural = "دسته‌های مهارت"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(SkillCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Skill(models.Model):
    """
    مدل مهارت برای ذخیره مهارت‌های حرفه‌ای.
    مهارت‌ها تنها توسط مدیر سیستم ایجاد و ویرایش می‌شوند؛ جویندگان کار از مهارت‌های موجود استفاده می‌کنند.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="نام مهارت",
        help_text="مثلاً Python, Java, طراحی گرافیک"
    )
    description = models.TextField(
        blank=True,
        verbose_name="توضیحات مهارت",
        help_text="شرح مختصر مهارت (اختیاری)"
    )
    icon = models.ImageField(
        upload_to='skill_icons/',
        null=True,
        blank=True,
        verbose_name="آیکون مهارت",
        help_text="تصویر یا آیکون مرتبط با این مهارت (اختیاری)"
    )
    website = models.URLField(
        blank=True,
        verbose_name="وبسایت",
        help_text="وبسایت مرتبط با مهارت (اختیاری)"
    )
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="دسته‌بندی",
        help_text="انتخاب دسته‌بندی مهارت (اختیاری)"
    )

    class Meta:
        verbose_name = "مهارت"
        verbose_name_plural = "مهارت‌ها"
        ordering = ['name']

    def __str__(self):
        return self.name




class EmployerProfile(models.Model):
    """
    پروفایل کارفرما به سبک لینکدین.
    شامل اطلاعات شرکت و اطلاعات تماس مربوط به کارفرمایان است.
    """
    user = models.OneToOneField(
        "Users.User",
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    company_name = models.CharField(
        max_length=255,
        verbose_name="نام شرکت",
        help_text="نام شرکت یا سازمان"
    )
    personal_info = models.OneToOneField(
        PersonalInformation,
        on_delete=models.CASCADE,
        verbose_name="اطلاعات شخصی",
        related_name="employer_personal_info"
    )
    id_card_info = models.OneToOneField(
        IdCardInformation,
        on_delete=models.CASCADE,
        verbose_name="اطلاعات کارت ملی",
        related_name="employer_id_card_info"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="بیوگرافی",
        help_text="توضیح مختصر درباره شرکت یا اهداف"
    )
    profile_picture = models.ImageField(
        upload_to='employers/profile_pics/',
        null=True,
        blank=True,
        verbose_name="تصویر پروفایل"
    )
    location = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="مکان"
    )
    industry = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="صنعت",
        help_text="حوزه فعالیت شغلی"
    )
    contact_email = models.EmailField(
        blank=True,
        verbose_name="ایمیل تماس"
    )
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="شماره تماس"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    class Meta:
        verbose_name = "پروفایل کارفرما"
        verbose_name_plural = "پروفایل‌های کارفرمایان"

    def __str__(self):
        return f"{self.company_name} - {self.user.username}"


class AdminProfile(models.Model):
    """
    پروفایل مدیر سیستم.
    مدیران معمولاً نیازی به اطلاعات حرفه‌ای پیچیده ندارند؛ اما فیلدهای مدیریتی اضافی می‌توانند در آینده افزوده شوند.
    """
    user = models.OneToOneField(
        "Users.User",
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    class Meta:
        verbose_name = "پروفایل مدیر"
        verbose_name_plural = "پروفایل‌های مدیران"

    def __str__(self):
        return f"{self.user.username} - Admin"


class SupportProfile(models.Model):
    """
    پروفایل پشتیبان سیستم.
    این مدل اطلاعات تخصص و ساعات کاری پشتیبان را ذخیره می‌کند.
    """
    user = models.OneToOneField(
        "Users.User",
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    class Meta:
        verbose_name = "پروفایل پشتیبان"
        verbose_name_plural = "پروفایل‌های پشتیبان"

    def __str__(self):
        return f"{self.user.username} - Support"
