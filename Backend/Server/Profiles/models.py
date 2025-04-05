from django.db import models

from Locations.models import City
from Industry.models import Industry



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

    kids_count = models.PositiveIntegerField(
        default=0,
        verbose_name="تعداد فرزند"
    )

    class Meta:
        verbose_name = "اطلاعات شخصی"
        verbose_name_plural = "اطلاعات شخصی"

    def __str__(self):
        return f"{self.get_gender_display()} - {self.age}"




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

    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        blank=True, 
        null=True, 
        verbose_name="صنعت"  # صنعت مربوطه (مانند فناوری، سلامت)
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

    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        blank=True, 
        null=True, 
        verbose_name="صنعت"  # صنعت مربوطه (مانند فناوری، سلامت)
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
