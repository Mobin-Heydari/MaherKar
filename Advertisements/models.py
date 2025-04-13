from django.db import models  # ایمپورت مدل‌های Django جهت تعریف مدل‌های دیتابیس

# ایمپورت مدل‌های مرتبط از اپ‌های دیگر
from Companies.models import Company           # وارد کردن مدل Company از اپ Companies
from Industry.models import Industry             # وارد کردن مدل Industry از اپ Industry
from Locations.models import City                # وارد کردن مدل City از اپ Locations
from Users.models import User                    # وارد کردن مدل User از اپ Users
from Profiles.models import JobSeekerProfile, EmployerProfile  # وارد کردن مدل‌های JobSeekerProfile و EmployerProfile از اپ Profiles
from Resumes.models import JobSeekerResume       # وارد کردن مدل JobSeekerResume از اپ Resumes
from Subscriptions.models import AdvertisementSubscription  # وارد کردن مدل AdvertisementSubscription از اپ Subscriptions




# =============================================================================
# مدل Advertisement (آگهی عمومی)
# =============================================================================
class Advertisement(models.Model):
    """
    مدل پایه برای آگهی‌ها با فیلدهای مشترک.
    این مدل شامل اطلاعات عمومی آگهی مانند عنوان، توضیحات، موقعیت، وضعیت و غیره است.
    """

    # ---------------------------
    # فیلدهای انتخابی (Choices) جهت نمایش محدوده حقوق، جنسیت، وضعیت سربازی، مدرک تحصیلی و وضعیت آگهی
    # ---------------------------
    class SalaryChoices(models.TextChoices):
        RANGE_5_TO_10 = '5 to 10', '5 تا 10 میلیون تومان'        # انتخاب محدوده حقوق از 5 تا 10 میلیون تومان
        RANGE_10_TO_15 = '10 to 15', '10 تا 15 میلیون تومان'      # انتخاب محدوده حقوق از 10 تا 15 میلیون تومان
        RANGE_15_TO_20 = '15 to 20', '15 تا 20 میلیون تومان'      # انتخاب محدوده حقوق از 15 تا 20 میلیون تومان
        RANGE_20_TO_30 = '20 to 30', '20 تا 30 میلیون تومان'      # انتخاب محدوده حقوق از 20 تا 30 میلیون تومان
        RANGE_30_TO_50 = '30 to 50', '30 تا 50 میلیون تومان'      # انتخاب محدوده حقوق از 30 تا 50 میلیون تومان
        MORE_THAN_50 = 'More than 50', 'بیش از 50 میلیون تومان'   # انتخاب محدوده حقوق بیش از 50 میلیون تومان
        NEGOTIABLE = 'Negotiable', 'توافقی'                        # انتخاب وضعیت توافقی برای حقوق

    class GenderChoices(models.TextChoices):
        MALE = 'Male', 'مرد'                 # انتخاب جنسیت مرد
        FEMALE = 'Female', 'زن'               # انتخاب جنسیت زن
        NOT_SPECIFIED = 'Not Specified', 'مهم نیست'  # انتخاب حالت "مهم نیست"

    class SoldierStatusChoices(models.TextChoices):
        COMPLETED = 'Completed', 'پایان خدمت'                 # انتخاب وضعیت سربازی: پایان خدمت
        PERMANENT_EXEMPTION = 'Permanent Exemption', 'معافیت دائم'  # انتخاب معافیت دائم
        EDUCATIONAL_EXEMPTION = 'Educational Exemption', 'معافیت تحصیلی'  # انتخاب معافیت تحصیلی
        NOT_SPECIFIED = 'Not Specified', 'مهم نیست'            # انتخاب حالت "مهم نیست" برای سربازی

    class DegreeChoices(models.TextChoices):
        BELOW_DIPLOMA = 'Below Diploma', 'زیر دیپلم'           # انتخاب حداقل مدرک زیر دیپلم
        DIPLOMA = 'Diploma', 'دیپلم'                             # انتخاب مدرک دیپلم
        ASSOCIATE = 'Associate', 'فوق دیپلم'                    # انتخاب مدرک فوق دیپلم
        BACHELOR = 'Bachelor', 'لیسانس'                         # انتخاب مدرک لیسانس
        MASTER = 'Master', 'فوق لیسانس'                         # انتخاب مدرک فوق لیسانس
        DOCTORATE = 'Doctorate', 'دکترا'                         # انتخاب مدرک دکترا

    class StatusChoices(models.TextChoices):
        PENDING = 'Pending', 'در حال بررسی'     # وضعیت آگهی: در حال بررسی
        APPROVED = 'Approved', 'تایید شده'         # وضعیت آگهی: تایید شده
        REJECTED = 'Rejected', 'رد شده'            # وضعیت آگهی: رد شده

    # ---------------------------
    # فیلدهای ارتباطی و اطلاعات کلیدی آگهی
    # ---------------------------
    industry = models.ForeignKey(
        Industry,                         # ارتباط آگهی با صنعت مربوطه
        on_delete=models.CASCADE,         # در صورت حذف صنعت، آگهی نیز حذف می‌شود
        related_name="Advertisements_Industry",  # نام رابطه معکوس برای دسترسی به آگهی‌های مربوط به صنعت
        verbose_name="صنعت"               # عنوان فیلد در پنل ادمین
    )

    owner = models.ForeignKey(
        User,                             # آگهی متعلق به یک کاربر (مالک)
        on_delete=models.CASCADE,         # در صورت حذف کاربر، آگهی نیز حذف می‌شود
        related_name="Advertisement_Owner",  # نام رابطه معکوس جهت دسترسی به آگهی‌های یک کاربر
        verbose_name="مالک"               # عنوان فیلد در پنل ادمین
    )

    subscription = models.OneToOneField(
        AdvertisementSubscription,        # آگهی به یک اشتراک مربوط می‌شود
        on_delete=models.CASCADE,         # در صورت حذف اشتراک، آگهی نیز حذف می‌شود
        related_name="Advertisements_Subscription",  # نام رابطه معکوس برای دسترسی به اشتراک آگهی
        verbose_name="اشتراک"             # عنوان فیلد
    )

    location = models.ForeignKey(
        City,                             # آگهی مربوط به یک شهر (موقعیت مکانی)
        on_delete=models.CASCADE,         # در صورت حذف شهر، آگهی نیز حذف می‌شود
        related_name="Advertisements_Location",  # نام رابطه معکوس جهت دسترسی به آگهی‌های مربوط به شهر
        verbose_name="موقعیت"              # عنوان فیلد
    )

    # ---------------------------
    # فیلدهای متنی و نمایشی
    # ---------------------------
    title = models.CharField(
        max_length=255,                   # حداکثر 255 کاراکتر برای عنوان آگهی
        verbose_name="عنوان آگهی"         # عنوان فیلد
    )

    slug = models.SlugField(
        max_length=255,                   # حداکثر طول 255 برای اسلاگ
        unique=True,                      # اسلاگ باید یکتا باشد (برای URL به کار می‌رود)
        verbose_name="اسلاگ"              # عنوان فیلد
    )

    advertise_code = models.CharField(
        max_length=220,                   # حداکثر 220 کاراکتر برای کد آگهی
        unique=True,                      # کد آگهی منحصربه‌فرد است
        db_index=True,                    # ایندکس در دیتابیس جهت جستجوی سریع‌تر
        verbose_name="کد آگهی",           # عنوان فیلد در پنل ادمین
        help_text="بعد از ثبت مقداردهی می‌شود"  # راهنمایی برای مقداردهی این فیلد
    )

    description = models.TextField(
        verbose_name="توضیحات بیشتر",     # توضیحات تکمیلی درباره آگهی
        blank=True,                       # قابلیت خالی گذاشتن فیلد
        null=True                         # امکان ذخیره مقدار NULL در دیتابیس
    )

    # ---------------------------
    # فیلدهای انتخابی (چند گزینه‌ای) برای وضعیت آگهی، جنسیت، وضعیت سربازی، مدرک تحصیلی و حقوق
    # ---------------------------
    status = models.CharField(
        max_length=20,                    # حداکثر 20 کاراکتر
        choices=StatusChoices.choices,    # استفاده از گزینه‌های تعریف‌شده در StatusChoices
        default=StatusChoices.PENDING,    # وضعیت پیش‌فرض آگهی (در حال بررسی)
        verbose_name="وضعیت آگهی"         # عنوان فیلد
    )

    gender = models.CharField(
        max_length=20,                    # حداکثر 20 کاراکتر برای جنسیت
        choices=GenderChoices.choices,    # استفاده از گزینه‌های تعریف‌شده در GenderChoices
        verbose_name="جنسیت"              # عنوان فیلد
    )

    soldier_status = models.CharField(
        max_length=30,                    # حداکثر 30 کاراکتر برای وضعیت سربازی
        choices=SoldierStatusChoices.choices,  # گزینه‌های مربوط به وضعیت سربازی
        verbose_name="وضعیت سربازی"      # عنوان فیلد
    )

    degree = models.CharField(
        max_length=20,                    # حداکثر 20 کاراکتر برای مدرک تحصیلی
        choices=DegreeChoices.choices,    # استفاده از گزینه‌های تعریف‌شده در DegreeChoices
        verbose_name="حداقل مدرک تحصیلی"  # عنوان فیلد
    )

    salary = models.CharField(
        max_length=20,                    # حداکثر 20 کاراکتر برای محدوده حقوق
        choices=SalaryChoices.choices,    # استفاده از گزینه‌های تعریف‌شده در SalaryChoices
        default=SalaryChoices.NEGOTIABLE, # مقدار پیش‌فرض: توافقی
        verbose_name="محدوده حقوق"       # عنوان فیلد
    )

    # ---------------------------
    # فیلدهای زمان‌بندی
    # ---------------------------
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")  # زمان ایجاد پیوست به صورت خودکار تنظیم می‌شود
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")  # زمان آخرین بروزرسانی پیوست به‌روز می‌شود

    class Meta:
        ordering = ["-created_at"]  # مرتب‌سازی آگهی‌ها به صورت نزولی بر اساس تاریخ ایجاد

    def __str__(self):
        return self.title   # متد __str__، عنوان آگهی را به عنوان نماینده شیء برمی‌گرداند



# =============================================================================
# مدل JobAdvertisement (آگهی کارفرما)
# =============================================================================
class JobAdvertisement(models.Model):
    """
    مدل برای آگهی‌های کارفرما. این مدل اطلاعات بیشتری مانند شرکت و کارفرما را در بر می‌گیرد.
    """

    advertisement = models.ForeignKey(
        Advertisement,                    # ارتباط با مدل Advertisement (آگهی عمومی)
        on_delete=models.CASCADE,         # در صورت حذف آگهی، این رکورد نیز حذف می‌شود
        verbose_name="آگهی",               # عنوان فیلد در پنل ادمین
        related_name="Job_Advertisement"   # نام رابطه معکوس جهت دسترسی به آگهی‌های کارفرما از Advertisement
    )

    company = models.ForeignKey(
        Company,                          # ارتباط با مدل Company جهت مشخص کردن شرکت مربوطه
        on_delete=models.CASCADE,         # در صورت حذف شرکت، این رکورد حذف می‌شود
        related_name="Company_Advertisement",  # نام رابطه معکوس برای دستیابی به آگهی‌های شرکت
        verbose_name="شرکت"               # عنوان فیلد
    )

    employer = models.ForeignKey(
        EmployerProfile,                  # ارتباط با مدل EmployerProfile جهت مشخص کردن کارفرمای آگهی
        on_delete=models.CASCADE,         # در صورت حذف کارفرما، رکورد حذف می‌شود
        related_name="Employer_Advertisement",  # نام رابطه معکوس جهت دستیابی به آگهی‌های کارفرما
        verbose_name="کارفرما"             # عنوان فیلد
    )

    job_type = models.CharField(
        max_length=20,                    # حداکثر 20 کاراکتر برای نوع کار
        choices=[
            ('Full-Time', 'تمام وقت'),    # انتخاب "تمام وقت"
            ('Part-Time', 'پاره وقت'),      # انتخاب "پاره وقت"
            ('Remote', 'دورکاری'),          # انتخاب "دورکاری"
            ('Internship', 'کارآموزی')        # انتخاب "کارآموزی"
        ],
        verbose_name="نوع کار"            # عنوان فیلد
    )

    description_position = models.TextField(
        verbose_name="موقعیت شغلی"         # توضیح متنی درباره موقعیت شغلی مربوط به آگهی
    )

    class Meta:
        verbose_name = "آگهی کارفرما"           # نام نمایشی مفرد برای مدل
        verbose_name_plural = "آگهی‌های کارفرما"  # نام نمایشی جمع برای مدل

    def __str__(self):
        # توجه: در اینجا به اشتباه از self.title استفاده شده؛ به جای آن می‌بایست از self.advertisement.title استفاده شود.
        return f"{self.advertisement.title} ({self.company.name})"  # نمایش عنوان آگهی (از Advertisement) و نام شرکت



# =============================================================================
# مدل ResumeAdvertisement (آگهی رزومه کارجو)
# =============================================================================
class ResumeAdvertisement(models.Model):
    """
    مدل برای آگهی‌های رزومه کارجو که آگهی‌های ارسال شده از سوی جویندگان کار را مدیریت می‌کند.
    """

    advertisement = models.ForeignKey(
        Advertisement,                   # ارتباط با مدل Advertisement برای آگهی عمومی
        on_delete=models.CASCADE,        # در صورت حذف آگهی، این رکورد حذف می‌شود
        verbose_name="آگهی",              # عنوان فیلد
        related_name="Resume_Advertisement"  # نام رابطه معکوس جهت دستیابی به آگهی‌های رزومه کارجو
    )

    job_seeker_profile = models.ForeignKey(
        JobSeekerProfile,                # ارتباط با مدل JobSeekerProfile جهت مشخص کردن پروفایل کارجو
        on_delete=models.CASCADE,        # در صورت حذف این پروفایل، رکورد حذف می‌شود
        related_name="Profile",           # نام رابطه معکوس جهت دستیابی به آگهی‌های رزومهٔ کارجو از طریق پروفایل
        verbose_name="پروفایل کارجو"       # عنوان فیلد
    )

    resume = models.ForeignKey(
        JobSeekerResume,                 # ارتباط با مدل JobSeekerResume جهت ذخیره رزومه ارسال شده
        on_delete=models.CASCADE,        # در صورت حذف رزومه، رکورد حذف می‌شود
        related_name="Resume",           # نام رابطه معکوس جهت دسترسی به آگهی‌های رزومه
        verbose_name="رزومه"              # عنوان فیلد
    )

    job_type = models.CharField(
        max_length=20,                   # حداکثر 20 کاراکتر برای نوع کار
        choices=[
            ('Full-Time', 'تمام وقت'),    # انتخاب "تمام وقت"
            ('Part-Time', 'پاره وقت'),      # انتخاب "پاره وقت"
            ('Remote', 'دورکاری'),          # انتخاب "دورکاری"
            ('Internship', 'کارآموزی')        # انتخاب "کارآموزی"
        ],
        verbose_name="نوع کار"            # عنوان فیلد
    )

    class Meta:
        verbose_name = "آگهی رزومه کارجو"          # نام نمایشی مفرد
        verbose_name_plural = "آگهی‌های رزومه کارجو"  # نام نمایشی جمع

    def __str__(self):
        # توجه: مانند مدل JobAdvertisement، بهتر است از self.advertisement.title استفاده شود.
        return f"{self.advertisement.title} ({self.job_seeker_profile})"  # نمایش عنوان آگهی و پروفایل کارجو



# =============================================================================
# مدل Application (درخواست)
# =============================================================================
class Application(models.Model):
    """
    مدل درخواست ارسال شده توسط جویندگان کار جهت ثبت‌نام در آگهی‌های شغلی.
    شامل وضعیت درخواست، نامه پوششی، پیوست رزومه و سایر جزئیات می‌باشد.
    """
    
    # تعریف گزینه‌های وضعیت درخواست با استفاده از TextChoices
    class StatusChoices(models.TextChoices):
        PENDING = 'PE', 'در انتظار'             # وضعیت "در انتظار" با کد 'PE'
        IN_REVIEW = 'IR', 'در حال بررسی'         # وضعیت "در حال بررسی" با کد 'IR'
        ACCEPTED = 'AC', 'پذیرفته شده'            # وضعیت "پذیرفته شده" با کد 'AC'
        REJECTED = 'RE', 'رد شده'                 # وضعیت "رد شده" با کد 'RE'
    
    # فیلد مربوط به پروفایل جوینده کار (JobSeekerProfile)
    job_seeker = models.ForeignKey(
        JobSeekerProfile,             # ارتباط با مدل JobSeekerProfile
        on_delete=models.CASCADE,     # در صورت حذف پروفایل، درخواست نیز حذف می‌شود
        related_name="Applications"   # نام رابطه معکوس برای دسترسی به درخواست‌های یک جوینده
    )
    
    # فیلد مربوط به آگهی کارفرما (JobAdvertisement)
    advertisement = models.ForeignKey(
        JobAdvertisement,             # ارتباط با مدل JobAdvertisement که درخواست مربوط به آن ارسال می‌شود
        on_delete=models.CASCADE,     # در صورت حذف آگهی، درخواست نیز حذف می‌شود
        related_name="Applications"   # نام رابطه معکوس جهت دسترسی به درخواست‌های یک آگهی
    )
    
    # فیلد متنی برای نگهداری نامه پوششی
    cover_letter = models.TextField(blank=True)
    # این فیلد جهت ارسال نامه پوششی توسط جوینده کار استفاده می‌شود؛ در صورت نیاز خالی باقی می‌ماند
    
    # فیلدی جهت نگهداری رزومه ارسال‌شده توسط جوینده کار
    resume = models.ForeignKey(
        JobSeekerResume,              # ارتباط رزومه با مدل JobSeekerResume
        on_delete=models.SET_NULL,    # در صورت حذف رزومه، مقدار این فیلد به NULL تنظیم می‌شود
        null=True                     # اجازه ذخیره مقدار null در این فیلد
    )
    
    # فیلد وضعیت درخواست با استفاده از گزینه‌های تعریف‌شده در StatusChoices
    status = models.CharField(
        max_length=20,                                    # حداکثر 20 کاراکتر
        choices=StatusChoices.choices,                    # استفاده از مقادیر پیش‌فرض تعریف‌شده (PENDING, IN_REVIEW, ACCEPTED, REJECTED)
        default=StatusChoices.PENDING                     # مقدار پیش‌فرض درخواست "در انتظار" است
    )
    
    # فیلد متنی جهت ذخیره یادداشت‌های کارفرما درباره درخواست
    employer_notes = models.TextField(blank=True, null=True)
    # این فیلد می‌تواند خالی بماند و در صورت نیاز اطلاعات تکمیلی کارفرما را نگهداری می‌کند
    
    # فیلد بولی جهت مشخص کردن اینکه آیا درخواست توسط کارفرما مشاهده شده است یا خیر
    viewed_by_employer = models.BooleanField(default=False)
    
    # فیلد زمان ایجاد درخواست؛ به صورت خودکار مقداردهی می‌شود
    created_at = models.DateTimeField(auto_now_add=True)
    # فیلد زمان به‌روزرسانی درخواست؛ به صورت خودکار در هر بروزرسانی تغییر می‌کند
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        # متد __str__ نمایشی از درخواست را برمی‌گرداند؛ شامل نام کاربری جوینده (از طریق job_seeker.user.username)
        # و عنوان آگهی (از Advertisement) می‌باشد.
        return f"{self.job_seeker.user.username} -> {self.advertisement.title}"
    
    def mark_as_viewed(self):
        """
        علامت‌گذاری درخواست به عنوان مشاهده شده توسط کارفرما.
        این متد، فیلد viewed_by_employer را به True تغییر می‌دهد و تغییرات را ذخیره می‌کند.
        """
        self.viewed_by_employer = True       # تغییر وضعیت مشاهده شدن به True
        self.save()                          # ذخیره تغییرات در دیتابیس
    
    def get_status_display_verbose(self):
        """
        دریافت توضیحات وضعیت درخواست به صورت متنی.
        متد get_status_display() به‌طور خودکار بر اساس choices وضعیت، متن نمایشی (verbose) وضعیت را برمی‌گرداند.
        """
        return self.get_status_display()     # برگرداندن توضیحات وضعیت (مانند "در انتظار"، "در حال بررسی" و غیره)
