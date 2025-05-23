from django.db import models  # وارد کردن ماژول مدل‌های Django جهت ساخت مدل‌های دیتابیس

# ایمپورت مدل‌های مرتبط از برنامه‌های دیگر:
from Locations.models import City     # وارد کردن مدل City از اپ Locations برای ذخیره اطلاعات شهر
from Industry.models import Industry    # وارد کردن مدل Industry از اپ Industry جهت ذخیره اطلاعات صنعت


# مدل اطلاعات شخصی کاربر
class PersonalInformation(models.Model):
    # تعریف کلاس داخلی برای تعیین جنسیت کاربر با استفاده از TextChoices
    class Gender(models.TextChoices):
        WOMEN = 'W', 'خانوم'  # گزینه: خانوم
        MAN = 'M', 'آقا'      # گزینه: آقا

    # فیلد جنسیت: یک فیلد ذخیره رشته‌ای با حداکثر یک کاراکتر؛ از گزینه‌های تعریف‌شده در Gender استفاده می‌کند
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        verbose_name="جنسیت",
        default=Gender.MAN  # مقدار پیش‌فرض: آقا
    )

    # فیلد سن: فقط اعداد صحیح مثبت را می‌پذیرد؛ پیش‌فرض 18 سال تعیین شده است
    age = models.PositiveIntegerField(
        verbose_name="سن",
        default=18
    )

    # فیلد تعداد فرزند: هم اعداد صحیح مثبت را می‌پذیرد؛ پیش‌فرض 0 است
    kids_count = models.PositiveIntegerField(
        default=0,
        verbose_name="تعداد فرزند"
    )

    # متادیتا (تنظیمات اضافی) مدل
    class Meta:
        verbose_name = "اطلاعات شخصی"          # نام نمایشی مدل به صورت مفرد
        verbose_name_plural = "اطلاعات شخصی"     # نام نمایشی مدل به صورت جمع

    # تابع نمایشی برای نمایش نمونه‌های مدل به صورت رشته‌ای؛ به عنوان مثال در پنل ادمین
    def __str__(self):
        return f"{self.get_gender_display()} - {self.age}"
        # get_gender_display()، مقدار خوانا (مانند "آقا" یا "خانوم") براساس انتخاب کاربر را باز می‌گرداند


# مدل پروفایل جوینده کار (شبیه به پروفایل لینکدین)
class JobSeekerProfile(models.Model):
    """
    پروفایل جوینده کار به سبک لینکدین.
    شامل اطلاعات حرفه‌ای و شخصی برای جویندگان کار.
    """
    # فیلد user: ارتباط یک به یک با مدل کاربر؛ در صورت حذف کاربر، پروفایل نیز حذف می‌شود
    user = models.OneToOneField(
        "Users.User",  # ارجاع به مدل کاربر در اپ Users
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )

    # فیلد personal_info: ارتباط یک به یک با مدل اطلاعات شخصی جهت ذخیره اطلاعات تکمیلی شخصی
    personal_info = models.OneToOneField(
        PersonalInformation,
        on_delete=models.CASCADE,
        verbose_name="اطلاعات شخصی",
        related_name="jobseeker_personal_info"  # نام رابطه معکوس جهت دسترسی از سمت اطلاعات شخصی به این پروفایل
    )

    # فیلد headline: عنوان شغلی کوتاه کاربر
    headline = models.CharField(
        max_length=255,
        verbose_name="عنوان شغلی",
        help_text="عنوان شغلی کوتاه (الزامی)"
    )

    # فیلد bio: بیوگرافی یا توضیح مختصر درباره کاربر؛ این فیلد اختیاری است
    bio = models.TextField(
        blank=True,
        verbose_name="بیوگرافی",
        help_text="توضیح مختصر درباره خودتان"
    )

    # فیلد profile_picture: تصویر پروفایل کاربر؛ فایل‌های آپلود شده در مسیر مشخص ذخیره می‌شوند
    profile_picture = models.ImageField(
        upload_to='jobseekers/profile_pics/',
        null=True,
        blank=True,
        verbose_name="تصویر پروفایل"
    )

    # فیلد location: ارجاع به مدل City جهت ذخیره شهر محل سکونت کاربر؛ در صورت حذف شهر، مقدار به NULL تنظیم می‌شود
    location = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="شهر"
    )

    # فیلد industry: ارجاع به مدل Industry جهت ذخیره صنعتی که در آن فعالیت می‌کند؛
    # در صورت حذف صنعت، مقدار این فیلد به NULL تنظیم می‌شود
    industry = models.ForeignKey(
        Industry,
        on_delete=models.SET_NULL,
        blank=True, 
        null=True, 
        verbose_name="صنعت"  # صنعت مربوطه (مانند فناوری، سلامت)
    )

    # فیلد created_at: تاریخ و زمان ایجاد پروفایل؛ به صورت خودکار در زمان ایجاد ثبت می‌شود
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    # فیلد updated_at: تاریخ و زمان به‌روزرسانی پروفایل؛ در هر تغییر خودکار به‌روزرسانی می‌شود
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    # متادیتای مدل پروفایل جوینده کار
    class Meta:
        verbose_name = "پروفایل جوینده کار"                   # نام مفرد پروفایل جوینده کار
        verbose_name_plural = "پروفایل‌های جویندگان کار"       # نام جمع پروفایل‌های جویندگان کار

    # تابع نمایش نمونه‌ها برای نمایش اطلاعات به صورت رشته‌ای
    def __str__(self):
        return f"{self.user.username} - پروفایل جوینده کار"


# مدل پروفایل کارفرما به سبک لینکدین
class EmployerProfile(models.Model):
    """
    پروفایل کارفرما به سبک لینکدین.
    شامل اطلاعات شرکت و اطلاعات تماس مربوط به کارفرمایان است.
    """
    # فیلد user: ارتباط یک به یک با مدل کاربر؛ در صورت حذف کاربر، پروفایل نیز حذف می‌شود
    user = models.OneToOneField(
        "Users.User",
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )

    # فیلد personal_info: ارتباط یک به یک با مدل اطلاعات شخصی جهت ذخیره اطلاعات تکمیلی مدیرعامل یا مسئول شرکت
    personal_info = models.OneToOneField(
        PersonalInformation,
        on_delete=models.CASCADE,
        verbose_name="اطلاعات شخصی",
        related_name="employer_personal_info"  # نام رابطه معکوس برای دسترسی از سمت اطلاعات شخصی به این پروفایل
    )

    # فیلد bio: توضیحات مختصر درباره شرکت یا اهداف آن
    bio = models.TextField(
        blank=True,
        verbose_name="بیوگرافی",
        help_text="توضیح مختصر درباره شرکت یا اهداف"
    )

    # فیلد profile_picture: تصویر پروفایل شرکت؛ فایل‌ها در مسیر مشخص ذخیره می‌شوند
    profile_picture = models.ImageField(
        upload_to='employers/profile_pics/',
        null=True,
        blank=True,
        verbose_name="تصویر پروفایل"
    )

    # فیلد location: ارجاع به مدل City جهت ذخیره مکان شرکت؛ در صورت حذف شهر، مقدار به NULL تنظیم می‌شود
    location = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="مکان"
    )

    # فیلد industry: ارجاع به مدل Industry جهت ذخیره صنعتی که شرکت در آن فعالیت می‌کند
    industry = models.ForeignKey(
        Industry,
        on_delete=models.SET_NULL,
        blank=True, 
        null=True, 
        verbose_name="صنعت"  # صنعت مربوطه (مانند فناوری، سلامت)
    )

    # فیلد created_at: تاریخ و زمان ایجاد پروفایل کارفرما
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    # فیلد updated_at: تاریخ و زمان به‌روزرسانی پروفایل کارفرما؛ به صورت خودکار به‌روزرسانی می‌شود
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    # تنظیمات اضافی مدل پروفایل کارفرما
    class Meta:
        verbose_name = "پروفایل کارفرما"                   # نام مفرد پروفایل کارفرما
        verbose_name_plural = "پروفایل‌های کارفرمایان"      # نام جمع پروفایل‌های کارفرمایان

    # تابع نمایش نمونه‌ها به صورت رشته‌ای
    def __str__(self):
        return f"{self.company_name} - {self.user.username}"


# مدل پروفایل مدیر سیستم
class AdminProfile(models.Model):
    """
    پروفایل مدیر سیستم.
    مدیران معمولاً نیازی به اطلاعات حرفه‌ای پیچیده ندارند؛ اما فیلدهای مدیریتی اضافی می‌توانند در آینده افزوده شوند.
    """
    # فیلد user: ارتباط یک به یک با مدل کاربر؛ در صورت حذف کاربر، این پروفایل نیز حذف می‌شود
    user = models.OneToOneField(
        "Users.User",
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )

    # فیلد created_at: تاریخ و زمان ایجاد پروفایل مدیر
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    # فیلد updated_at: تاریخ و زمان به‌روزرسانی پروفایل مدیر
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    # تنظیمات اضافی مدل پروفایل مدیر
    class Meta:
        verbose_name = "پروفایل مدیر"
        verbose_name_plural = "پروفایل‌های مدیران"

    # تابع نمایش نمونه‌های مدل مدیر به صورت رشته‌ای
    def __str__(self):
        return f"{self.user.username} - Admin"


# مدل پروفایل پشتیبان سیستم
class SupportProfile(models.Model):
    """
    پروفایل پشتیبان سیستم.
    این مدل اطلاعات تخصص و ساعات کاری پشتیبان را ذخیره می‌کند.
    """
    # فیلد user: ارتباط یک به یک با مدل کاربر؛ در صورت حذف کاربر، پروفایل پشتیبان نیز حذف می‌شود
    user = models.OneToOneField(
        "Users.User",
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )

    # فیلد created_at: تاریخ و زمان ایجاد پروفایل پشتیبان
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    # فیلد updated_at: تاریخ و زمان به‌روزرسانی پروفایل پشتیبان؛ در هر تغییر به‌روزرسانی می‌شود
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    # تنظیمات اضافی مدل پروفایل پشتیبان
    class Meta:
        verbose_name = "پروفایل پشتیبان"
        verbose_name_plural = "پروفایل‌های پشتیبان"

    # تابع نمایش نمونه‌ها به صورت رشته‌ای
    def __str__(self):
        return f"{self.user.username} - Support"
