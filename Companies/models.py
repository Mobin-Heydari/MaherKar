from django.db import models  # وارد کردن ماژول مدل‌های Django جهت تعریف مدل‌های دیتابیس
from django.utils.text import slugify  # وارد کردن تابع slugify جهت تولید اسلاگ از رشته (مثلاً نام شرکت)

# ایمپورت مدل‌های مرتبط از اپ‌های دیگر:
from Locations.models import City       # ایمپورت مدل City از اپ Locations جهت ذخیره اطلاعات شهر
from Industry.models import Industry      # ایمپورت مدل Industry از اپ Industry جهت ذخیره اطلاعات صنعت

import uuid



  
class Company(models.Model):
    # -------------------------------
    # فیلد مربوط به مدیرعامل شرکت
    # -------------------------------

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)

    employer = models.ForeignKey(
        'Users.User',  # ارجاع به مدل User از اپ Users
        on_delete=models.CASCADE,  # در صورت حذف مدیرعامل، شرکت نیز حذف می‌شود
        verbose_name="مدیرعامل"  # نام نمایشی فیلد در پنل ادمین
    )

    # -------------------------------
    # فیلدهای اطلاعات پایه شرکت
    # -------------------------------
    name = models.CharField(
        max_length=255, 
        unique=True,  # نام شرکت باید یکتا باشد
        verbose_name="نام شرکت"  # نام شرکت جهت نمایش در پنل
    )
    description = models.TextField(
        blank=True,  # توضیحات اختیاری است
        null=True,   # امکان ذخیره مقدار None فراهم شده است
        verbose_name="توضیحات"  # توضیحات شرکت
    )
    website = models.URLField(
        blank=True,  # وبسایت اختیاری است
        null=True,
        verbose_name="وبسایت"  # لینک وبسایت شرکت
    )
    email = models.EmailField(
        blank=True,  # ایمیل اختیاری می‌باشد
        null=True,
        verbose_name="ایمیل"  # ایمیل رسمی شرکت
    )
    phone_number = models.CharField(
        max_length=20, 
        blank=True,  # شماره تماس اختیاری
        null=True,
        verbose_name="شماره تماس"  # شماره تماس شرکت
    )

    # -------------------------------
    # فیلدهای رسانه‌ای شرکت
    # -------------------------------
    logo = models.ImageField(
        upload_to='company/logos/',  # مسیر ذخیره لوگوی شرکت در پوشه‌ی تعیین شده
        blank=True,  # لوگو اختیاری است
        null=True,
        verbose_name="لوگو"  # نمایش عنوان فیلد
    )
    banner = models.ImageField(
        upload_to='company/banners/',  # مسیر ذخیره بنر شرکت
        blank=True,
        null=True,
        verbose_name="بنر"  # عنوان نمایشی فیلد
    )
    intro_video = models.FileField(
        upload_to='company/videos/',  # مسیر ذخیره ویدئوی معرفی
        blank=True,
        null=True,
        verbose_name="ویدئوی معرفی"  # عنوان نمایشی فیلد ویدئو
    )

    # -------------------------------
    # آدرس و مکان شرکت
    # -------------------------------
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name="آدرس"  # آدرس کامل شرکت
    )
    location = models.ForeignKey(
        City,  # ارتباط با مدل City جهت تعیین شهر شرکت
        on_delete=models.CASCADE,  # در صورت حذف شهر، شرکت نیز حذف می‌شود
        max_length=100,            # محدودیت طول رشته (این مقدار معمولاً در فیلد ForeignKey کاربرد ندارد)
        verbose_name="شهر"  # نمایش عنوان فیلد
    )
    postal_code = models.CharField(
        max_length=20, 
        blank=True,
        null=True,
        verbose_name="کد پستی"  # کد پستی شرکت
    )

    # -------------------------------
    # اطلاعات اضافی شرکت
    # -------------------------------
    founded_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="تاریخ تأسیس"  # تاریخی که شرکت تأسیس شده است
    )
    industry = models.ForeignKey(
        Industry,  # ارتباط با مدل Industry جهت تعیین صنعتی که شرکت در آن فعالیت می‌کند
        on_delete=models.CASCADE,  # در صورت حذف صنعت، شرکت نیز حذف می‌شود
        blank=True,
        null=True,
        verbose_name="صنعت"  # عنوان نمایشی فیلد
    )
    number_of_employees = models.IntegerField(
        blank=True,   # تعداد کارکنان اختیاری است
        null=True,
        verbose_name="تعداد کارکنان"  # تعداد کارکنان شرکت
    )

    # -------------------------------
    # اطلاعات شبکه‌های اجتماعی شرکت
    # -------------------------------
    linkedin = models.URLField(
        blank=True,
        null=True,
        verbose_name="لینک LinkedIn"  # لینک صفحه LinkedIn شرکت
    )
    twitter = models.URLField(
        blank=True,
        null=True,
        verbose_name="لینک Twitter"  # لینک صفحه Twitter شرکت
    )
    instagram = models.URLField(
        blank=True,
        null=True,
        verbose_name="لینک Instagram"  # لینک صفحه Instagram شرکت
    )

    # -------------------------------
    # زمان‌بندی‌ها (تاریخ ایجاد و به‌روزرسانی)
    # -------------------------------
    created_at = models.DateTimeField(
        auto_now_add=True,  # زمان ایجاد رکورد به‌طور خودکار ثبت می‌شود
        verbose_name="تاریخ ایجاد"  # عنوان نمایشی فیلد
    )
    updated_at = models.DateTimeField(
        auto_now=True,  # زمان آخرین به‌روزرسانی رکورد به‌روز می‌شود
        verbose_name="تاریخ بروزرسانی"  # عنوان نمایشی فیلد
    )

    # -------------------------------
    # متد نمایش (نمایش نام شرکت در پنل ادمین)
    # -------------------------------
    def __str__(self):
        return self.name  # بازگرداندن نام شرکت به عنوان نمایش نمونه

