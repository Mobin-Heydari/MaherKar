from django.db import models  # وارد کردن ماژول models از django برای تعریف مدل‌های دیتابیس
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin  # وارد کردن کلاس‌های پایه برای پیاده‌سازی مدل کاربر سفارشی
from .managers import UserManager  # وارد کردن مدیریت‌کننده سفارشی کاربر که در فایل managers تعریف شده است


# تعریف مدل برای اطلاعات کارت ملی کاربر
class IdCardInFormation(models.Model):
    # تعریف کلاس داخلی برای وضعیت‌های مختلف کارت ملی با استفاده از TextChoices
    class IdCardStatus(models.TextChoices):
        PENDING = 'P', 'در انتظار تایید'   # وضعیت: در انتظار تایید
        VERIFIED = 'V', 'تایید شده'         # وضعیت: تایید شده
        REJECTED = 'R', 'رد شده'             # وضعیت: رد شده

    # فیلد شماره ملی که یک رشته با حداکثر ۱۳ کاراکتر است؛ امکان خالی بودن یا تهی بودن داده نیز وجود دارد
    id_card_number = models.CharField(
        verbose_name="شماره ملی",  
        max_length=13,
        blank=True,   # اجازه می‌دهد این فیلد به صورت خالی ذخیره شود
        null=True,    # امکان ذخیره کردن مقدار None را فراهم می‌کند
    )

    # فیلد بارگذاری فایل کارت ملی جهت ذخیره تصویر یا اسکن کارت ملی
    id_card = models.FileField(
        upload_to='Users/id_cards/',  # مسیر ذخیره‌سازی فایل‌های کارت ملی
        verbose_name="کارت ملی",
        help_text="بارگذاری تصویر/اسکن کارت ملی",  # متن راهنما برای کاربر
        blank=True,  # امکان خالی بودن فیلد در فرم‌ها
        null=True,   # اجازه ذخیره مقدار تهی برای این فیلد
    )

    # فیلد وضعیت کارت ملی که از بین گزینه‌های تعریف شده در IdCardStatus انتخاب می‌شود
    id_card_status = models.CharField(
        max_length=1,  # طول رشته تنها یک کاراکتر است که کد وضعیت را ذخیره می‌کند
        choices=IdCardStatus.choices,  # گزینه‌های مجاز برای وضعیت کارت ملی
        default=IdCardStatus.PENDING,  # تنظیم وضعیت پیشفرض به "در انتظار تایید"
        verbose_name="وضعیت کارت ملی",
        help_text="وضعیت بررسی کارت ملی"  # توضیح مختصر درباره فیلد وضعیت کارت ملی
    )

    # متادیتا یا تنظیمات اضافی برای مدل
    class Meta:
        verbose_name = "اطلاعات کارت ملی"  # نام مفردی که در پنل مدیریت نمایش داده می‌شود
        verbose_name_plural = "اطلاعات کارت ملی"  # نام جمعی که در پنل مدیریت نمایش داده می‌شود

    # تابع تبدیل نمونه به رشته؛ معمولاً در پنل مدیریت یا برای نمایش نمایشی از مدل استفاده می‌شود
    def __str__(self):
        # نمایش شماره ملی در صورت موجودیت، و در غیر اینصورت نمایش "No ID"
        id_val = self.id_card_number if self.id_card_number else "No ID"
        # استفاده از متد get_id_card_status_display برای نمایش وضعیت کارت ملی به صورت خوانا
        return f"{id_val} - {self.get_id_card_status_display()}"


# تعریف مدل اصلی کاربر با استفاده از کلاس‌های AbstractBaseUser و PermissionsMixin
class User(AbstractBaseUser, PermissionsMixin):
    # تعریف کلاس داخلی برای نوع‌های کاربر (جویننده کار، کارفرما، پشتیبان یا مدیر)
    class UserTypes(models.TextChoices):
        JOB_SEEKER = "JS", "جوینده کار"   # تعریف نوع کاربر: جوینده کار
        EMPLOYER = "EM", "کارفرما"          # تعریف نوع کاربر: کارفرما
        SUPPORT = "SU", "پشتیبان"           # تعریف نوع کاربر: پشتیبان سیستم
        ADMIN = "AD", "مدیر"               # تعریف نوع کاربر: مدیر سیستم

    # تعریف کلاس داخلی برای وضعیت حساب کاربری
    class AccountStatus(models.TextChoices):
        ACTIVE = "ACT", "فعال"              # وضعیت: حساب فعال
        SUSPENDED = "SUS", "تعلیق شده"       # وضعیت: حساب تعلیق شده
        DELETED = "DEL", "حذف شده"           # وضعیت: حساب حذف شده

    # فیلد تعیین نوع کاربر که مقدار آن بر اساس گزینه‌های تعریف‌شده در UserTypes انتخاب می‌شود
    user_type = models.CharField(
        max_length=2,  # به دلیل اینکه کد‌های مربوطه ۲ کاراکتری هستند
        choices=UserTypes.choices,  # استفاده از گزینه‌های موجود برای نوع کاربر
        verbose_name="نوع کاربر",
    )

    # ایجاد ارتباط یک به یک با مدل IdCardInFormation جهت ذخیره اطلاعات کارت ملی کاربر
    id_card_info = models.OneToOneField(
        IdCardInFormation,   # مدل مرتبط اطلاعات کارت ملی
        on_delete=models.SET_NULL,  # در صورت حذف اطلاعات کارت ملی، مقدار این فیلد به NULL تنظیم می‌شود
        verbose_name="اطلاعات کارت ملی",
        related_name="id_card_info",  # نام رابطه معکوس برای دسترسی از طریق مدل اطلاعات کارت ملی
        null=True,  # امکان ذخیره مقدار تهی
        blank=True  # امکان خالی بودن فیلد در فرم‌ها
    )

    # فیلد وضعیت حساب کاربری که نشان‌دهنده وضعیت کلی حساب (فعال، تعلیق شده یا حذف شده) است
    status = models.CharField(
        max_length=3,  # به دلیل اینکه کدهای وضعیت سه کاراکتری هستند
        choices=AccountStatus.choices,  # انتخاب وضعیت از گزینه‌های تعریف‌شده
        default=AccountStatus.ACTIVE,  # وضعیت پیشفرض به عنوان "فعال" تنظیم شده است
        verbose_name="وضعیت حساب کاربری",
    )

    # فیلد ایمیل کاربر که به عنوان شناسه یکتا استفاده می‌شود
    email = models.EmailField(
        unique=True,  # تضمین یکتا بودن ایمیل
        verbose_name="ایمیل",
    )

    # فیلد شماره تلفن کاربر که به عنوان شناسه ورود و اطلاعات تماس استفاده خواهد شد
    phone = models.CharField(
        unique=True,  # شماره تلفن نباید تکراری باشد
        max_length=11,  # محدودیت تعداد ارقام شماره تلفن
        verbose_name="شماره تلفن",
    )

    # فیلد نام کاربری که باید یکتا باشد برای شناسایی کاربر در سیستم
    username = models.CharField(
        max_length=40,  # محدودیت تعداد حروف نام کاربری
        unique=True,  # تضمین یکتا بودن نام کاربری
        verbose_name="نام کاربری",
    )

    # فیلد نام و نام خانوادگی کاربر، که امکان خالی بودن نیز وجود دارد
    full_name = models.CharField(
        verbose_name="نام و نام خوانوادگی",
        max_length=255,  # حداکثر تعداد کاراکترهای مجاز
        null=True,   # اجازه ذخیره مقدار تهی
        blank=True,  # امکان عدم وارد کردن نام کامل
    )

    # فیلد تاریخ عضویت که به صورت خودکار در زمان ایجاد کاربر تنظیم می‌شود
    joined_date = models.DateField(
        auto_now_add=True,  # تاریخ عضویت مستقیم در هنگام ایجاد کاربر ثبت می‌شود
        verbose_name="تاریخ عضویت",
    )

    # فیلد تاریخ آخرین به‌روزرسانی اطلاعات کاربر که به صورت خودکار در هر تغییر بروزرسانی می‌شود
    last_updated = models.DateTimeField(
        auto_now=True,  # به‌روزرسانی خودکار زمان در هر تغییر
        verbose_name="تاریخ آخرین به‌روزرسانی",
    )

    # فیلد وضعیت فعال بودن حساب که مشخص می‌کند آیا حساب کاربر فعال است یا خیر
    is_active = models.BooleanField(
        default=True,  # پیشفرض حساب به صورت فعال تعریف شده است
        verbose_name="فعال",
    )

    # فیلد مشخص‌کننده‌ی مدیر بودن کاربر؛ یعنی آیا کاربر دسترسی‌های مدیر سیستم را دارد یا خیر
    is_admin = models.BooleanField(
        default=False,  # پیشفرض کاربر مدیر نیست
        verbose_name="مدیر",
    )

    # تعیین فیلد اصلی برای ورود به سیستم؛ در اینجا شماره تلفن بعنوان شناسه اصلی استفاده می‌شود
    USERNAME_FIELD = "phone"

    # فیلدهای ضروری برای ایجاد کاربر جدید به جز فیلد اصلی
    REQUIRED_FIELDS = ["username", "email", "full_name"]

    # اختصاص شی مدیریت سفارشی جهت ایجاد، ویرایش و مدیریت کاربران
    objects = UserManager()

    # تنظیمات تکمیلی مدل در کلاس Meta
    class Meta:
        ordering = ['joined_date']  # ترتیب نمایش کاربران بر اساس تاریخ عضویت (از قدیم به جدید یا برعکس)
        verbose_name = "کاربر"  # نام مفرد مدل جهت نمایش در پنل مدیریت
        verbose_name_plural = "کاربران"  # نام جمع مدل جهت نمایش در پنل مدیریت

    # تابع تبدیل نمونه کاربر به رشته جهت نمایش (اینجا از نام کاربری استفاده می‌شود)
    def __str__(self):
        return self.username

    # تابع تعیین مجوز دسترسی فرد؛ در اینجا تنها اگر کاربر مدیر باشد، مجوزهای مربوطه را دارد
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # تابع بررسی مجوز دسترسی کاربر به اپلیکیشن‌ها؛ مدیر دسترسی کامل دارند
    def has_module_perms(self, app_label):
        return self.is_admin

    # خصوصیتی برای نشان دادن اینکه آیا کاربر عضو کارکنان (staff) محسوب می‌شود یا خیر؛
    # در این پیاده‌سازی کاربر مدیر به عنوان کارکنان در نظر گرفته می‌شود
    @property
    def is_staff(self):
        return self.is_admin
