from django.db import models
from django.utils.text import slugify




class JobSeekerProfile(models.Model):
    """
    پروفایل جوینده کار به سبک لینکدین.
    شامل اطلاعات حرفه‌ای و شخصی برای جویندگان کار است.
    """

    # جنسیت کارجو
    class Gender(models.TextChoices):
        WOMEN = 'W', 'خانوم'
        MAN = 'M', 'آقا'

    # وضعیت کارت ملی: وضعیت بررسی کارت ملی
    class IdCardStatus(models.TextChoices):
        PENDING = 'P', 'در انتظار تایید'
        VERIFIED = 'V', 'تایید شده'
        REJECTED = 'R', 'رد شده'

    # ارتباط یک به یک با مدل کاربر پایه
    user = models.OneToOneField(
        "Users.User",
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    # جنسیت کارجو
    gender = models.CharField(
        max_length=5,
        verbose_name="جنسیت",
        default=Gender.MAN
    )
    # سن
    age = models.PositiveIntegerField(
        verbose_name="سن",
        default=18
    )
    # تعداد فرزند
    kids_count = models.IntegerField(
        default=0,
        verbose_name="تعداد فرزند"
    )
    # عنوان شغلی: مثلاً "توسعه‌دهنده نرم‌افزار"
    headline = models.CharField(
        max_length=255,
        verbose_name="عنوان شغلی",
        help_text="عنوان شغلی کوتاه (الزامی)"
    )
    # بیوگرافی: توضیح مختصر در مورد تجربه و اهداف
    bio = models.TextField(
        verbose_name="بیوگرافی",
        help_text="توضیح مختصر درباره خودتان",
        blank=True
    )
    # تصویر پروفایل: آپلود تصویر کاربر
    profile_picture = models.ImageField(
        upload_to='jobseekers/profile_pics/',
        null=True,
        blank=True,
        verbose_name="تصویر پروفایل"
    )
    # مکان: شهر یا منطقه محل سکونت (الزامی)
    location = models.CharField(
        max_length=255,
        verbose_name="مکان",
        help_text="شهر یا منطقه محل سکونت (الزامی)"
    )
    # صنعت: حوزه فعالیت شغلی (اختیاری)
    industry = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="صنعت",
        help_text="حوزه فعالیت شغلی"
    )
    # ایمیل تماس: جهت نمایش (اختیاری)
    contact_email = models.EmailField(
        blank=True,
        verbose_name="ایمیل تماس"
    )
    # شماره تماس: جهت ارتباط (اختیاری)
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="شماره تماس"
    )
    # وب‌سایت: لینک شخصی یا نمونه‌کار آنلاین (اختیاری)
    website = models.URLField(
        blank=True,
        verbose_name="وب‌سایت"
    )
    # لینکدین: آدرس پروفایل لینکدین (اختیاری)
    linkedin_profile = models.URLField(
        blank=True,
        verbose_name="لینکدین"
    )
    # رزومه: آپلود فایل رزومه (الزامی)
    resume = models.FileField(
        upload_to='jobseekers/resumes/',
        verbose_name="رزومه",
        help_text="بارگذاری فایل رزومه (CV)"
    )
    # ترجیحات شغلی: نوع شغل مورد نظر (مثلاً تمام‌وقت یا پاره‌وقت) (اختیاری)
    job_type_preference = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="نوع شغل مورد نظر",
        help_text="مثلاً تمام‌وقت یا پاره‌وقت"
    )
    # حقوق مورد انتظار: مقدار عددی حقوق مورد انتظار (اختیاری)
    expected_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="حقوق مورد انتظار"
    )
    # فیلد کارت ملی: آپلود تصویر یا اسکن کارت ملی (الزامی)
    id_card = models.FileField(
        upload_to='jobseekers/id_cards/',
        verbose_name="کارت ملی",
        help_text="بارگذاری تصویر/اسکن کارت ملی (الزامی)"
    )
    # وضعیت کارت ملی: نشان‌دهنده وضعیت بررسی کارت ملی
    id_card_status = models.CharField(
        max_length=1,
        choices=IdCardStatus.choices,
        default=IdCardStatus.PENDING,
        verbose_name="وضعیت کارت ملی",
        help_text="وضعیت بررسی کارت ملی"
    )
    # رابطه چند به چند با مدل مهارت؛ کاربر می‌تواند مهارت‌های از پیش تعریف‌شده را انتخاب کند.
    skills = models.ManyToManyField(
        'Skill',
        blank=True,
        verbose_name="مهارت‌ها",
        help_text="انتخاب مهارت‌های مرتبط از بین مهارت‌های تعریف شده"
    )
    # تاریخ ایجاد پروفایل
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    # تاریخ به‌روزرسانی پروفایل
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
    # ارتباط با پروفایل جوینده کار
    job_seeker = models.ForeignKey(
        JobSeekerProfile,
        on_delete=models.CASCADE,
        related_name="experiences",
        verbose_name="جوینده کار"
    )
    # عنوان شغلی در این تجربه
    title = models.CharField(
        max_length=255,
        verbose_name="عنوان شغلی",
        help_text="عنوان شغلی یا نقش در این تجربه"
    )
    # نام شرکت یا سازمان
    company = models.CharField(
        max_length=255,
        verbose_name="شرکت"
    )
    # مکان شرکت (اختیاری)
    location = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="مکان"
    )
    # تاریخ شروع کار
    start_date = models.DateField(
        verbose_name="تاریخ شروع"
    )
    # تاریخ پایان (اختیاری؛ می‌تواند خالی باشد در صورت ادامه داشتن فعالیت)
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ پایان"
    )
    # توضیحات و شرح وظایف (اختیاری)
    description = models.TextField(
        blank=True,
        verbose_name="توضیحات"
    )

    class Meta:
        verbose_name = "تجربه کاری"
        verbose_name_plural = "تجربیات کاری"

    def __str__(self):
        return f"{self.title} at {self.company}"




class Education(models.Model):
    """
    مدل تحصیلات، مشابه بخش تحصیلات لینکدین.
    """
    # ارتباط با پروفایل جوینده کار
    job_seeker = models.ForeignKey(
        JobSeekerProfile,
        on_delete=models.CASCADE,
        related_name="educations",
        verbose_name="جوینده کار"
    )
    # نام دانشگاه یا مدرسه
    school = models.CharField(
        max_length=255,
        verbose_name="دانشگاه/مدرسه"
    )
    # مدرک تحصیلی دریافت شده
    degree = models.CharField(
        max_length=255,
        verbose_name="مدرک تحصیلی"
    )
    # رشته یا گرایش تحصیلی
    field_of_study = models.CharField(
        max_length=255,
        verbose_name="رشته تحصیلی"
    )
    # تاریخ شروع تحصیل
    start_date = models.DateField(
        verbose_name="تاریخ شروع"
    )
    # تاریخ پایان تحصیل (اختیاری)
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ پایان"
    )
    # توضیحات (اختیاری)
    description = models.TextField(
        blank=True,
        verbose_name="توضیحات"
    )

    class Meta:
        verbose_name = "تحصیلات"
        verbose_name_plural = "تحصیلات"

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} from {self.school}"




class SkillCategory(models.Model):
    """
    مدل دسته‌بندی مهارت‌ها.
    این مدل برای سازماندهی مهارت‌ها در دسته‌های مشخص مانند "برنامه نویسی"، "طراحی" و غیره استفاده می‌شود.
    """
    # نام دسته‌بندی؛ این فیلد باید یکتا باشد
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="نام دسته",
        help_text="نام دسته‌بندی مهارت (مثلاً 'برنامه نویسی' یا 'طراحی')"
    )
    # اسلاگ تولید شده از نام دسته؛ برای ایجاد URL دوستانه
    slug = models.SlugField(
        unique=True,
        verbose_name="اسلاگ دسته",
        help_text="اسلاگ برای دسته‌بندی که معمولاً از نام تولید می‌شود"
    )
    # آیکون مرتبط با دسته‌بندی (اختیاری)
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
        # در صورتی که اسلاگ وجود ندارد، از نام دسته استفاده کرده و به صورت خودکار تولید می‌شود.
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Skill(models.Model):
    """
    مدل مهارت برای ذخیره مهارت‌های حرفه‌ای.
    این مهارت‌ها تنها توسط مدیر سیستم ایجاد و ویرایش می‌شوند.
    کاربران (جویندگان کار) تنها می‌توانند از مهارت‌های موجود استفاده کنند.
    """
    # نام مهارت – باید یکتا باشد تا از تکراری شدن جلوگیری شود.
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="نام مهارت",
        help_text="مثلاً Python, Java, طراحی گرافیک"
    )
    # توضیحات اختیاری جهت شرح مهارت
    description = models.TextField(
        blank=True,
        verbose_name="توضیحات مهارت",
        help_text="شرح مختصر مهارت (اختیاری)"
    )
    # آیکون مرتبط با مهارت (اختیاری)
    icon = models.ImageField(
        upload_to='skill_icons/',
        null=True,
        blank=True,
        verbose_name="آیکون مهارت",
        help_text="تصویر یا آیکون مرتبط با این مهارت (اختیاری)"
    )
    # وبسایت مرتبط با مهارت (اختیاری)
    website = models.URLField(
        blank=True,
        verbose_name="وبسایت",
        help_text="وبسایت مرتبط با مهارت (اختیاری)"
    )
    # ارتباط مهارت با دسته‌بندی آن
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

    # ارتباط یک به یک با مدل کاربر پایه (کاربر باید از نوع کارفرما باشد)
    user = models.OneToOneField(
        "Users.User",
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    
    # نام شرکت: فیلد الزامی برای ذخیره نام شرکت
    company_name = models.CharField(
        max_length=255,
        verbose_name="نام شرکت",
        help_text="نام کامل شرکت (الزامی)"
    )
    
    # لوگوی شرکت: آپلود تصویر لوگو (اختیاری)
    company_logo = models.ImageField(
        upload_to='employers/logos/',
        null=True,
        blank=True,
        verbose_name="لوگوی شرکت",
        help_text="لوگوی شرکت (اختیاری)"
    )
    
    # وبسایت شرکت: آدرس اینترنتی شرکت (اختیاری)
    website = models.URLField(
        blank=True,
        verbose_name="وبسایت شرکت",
        help_text="آدرس وبسایت شرکت (اختیاری)"
    )
    
    # صنعت: حوزه فعالیت شرکت (اختیاری)
    industry = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="صنعت",
        help_text="حوزه فعالیت شرکت (اختیاری)"
    )
    
    # اندازه شرکت: اطلاعاتی مانند کوچک، متوسط یا بزرگ (اختیاری)
    company_size = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="اندازه شرکت",
        help_text="اندازه شرکت (مثلاً کوچک، متوسط، بزرگ) (اختیاری)"
    )
    
    # توضیحات شرکت: شرح مختصر درباره شرکت و خدمات آن (اختیاری)
    description = models.TextField(
        blank=True,
        verbose_name="توضیحات شرکت",
        help_text="شرح مختصری از شرکت و خدمات آن (اختیاری)"
    )
    
    # مکان شرکت: شهر یا منطقه محل شرکت (الزامی)
    location = models.CharField(
        max_length=255,
        verbose_name="مکان شرکت",
        help_text="شهر یا منطقه محل شرکت (الزامی)"
    )
    
    # ایمیل تماس شرکت: جهت ارتباط (اختیاری)
    contact_email = models.EmailField(
        blank=True,
        verbose_name="ایمیل تماس شرکت",
        help_text="ایمیل جهت تماس با شرکت (اختیاری)"
    )
    
    # شماره تماس شرکت: جهت ارتباط مستقیم (اختیاری)
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="شماره تماس شرکت",
        help_text="شماره تماس جهت ارتباط با شرکت (اختیاری)"
    )
    
    # تاریخ تأسیس شرکت: تاریخی که شرکت تأسیس شده است (اختیاری)
    established_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ تأسیس",
        help_text="تاریخ تأسیس شرکت (اختیاری)"
    )
    
    # تاریخ ایجاد پروفایل: به صورت خودکار هنگام ایجاد ثبت می‌شود
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    
    # تاریخ به‌روزرسانی پروفایل: به صورت خودکار هنگام آپدیت پروفایل تنظیم می‌شود
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
    مدیران معمولاً نیازی به اطلاعات حرفه‌ای پیچیده ندارند؛ اما ممکن است فیلدهایی مانند یادداشت‌های مدیریتی و سطح دسترسی داشته باشند.
    """

    # ارتباط یک به یک با مدل کاربر پایه؛ کاربر مربوط به مدیر باید از نوع "Admin" باشد.
    user = models.OneToOneField(
        "Users.User",
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    
    
    # تاریخ ایجاد پروفایل: ذخیره به صورت خودکار هنگام ایجاد
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    
    # تاریخ به‌روزرسانی پروفایل: به صورت خودکار هنگام به‌روزرسانی تنظیم می‌شود
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
    پشتیبان می‌تواند شامل حوزه تخصص، ساعات کاری و امتیازات ارزیابی شده باشد.
    """

    # ارتباط یک به یک با مدل کاربر؛ کاربر مربوط به پشتیبان باید از نوع "Support" باشد.
    user = models.OneToOneField(
        "Users.User",
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    
    
    # تاریخ ایجاد پروفایل: ثبت خودکار هنگام ایجاد
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    
    # تاریخ به‌روزرسانی پروفایل: ثبت خودکار هنگام به‌روزرسانی
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    class Meta:
        verbose_name = "پروفایل پشتیبان"
        verbose_name_plural = "پروفایل‌های پشتیبان"

    def __str__(self):
        return f"{self.user.username} - Support"
