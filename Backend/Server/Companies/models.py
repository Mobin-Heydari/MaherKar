from django.db import models
from django.utils.text import slugify

from Locations.models import City




class Company(models.Model):

    # ارتباط با مدل مدیرعامل
    employer = models.ForeignKey(
        'Users.User',
        on_delete=models.CASCADE,
        verbose_name="مدیرعامل"
    )

    # اطلاعات پایه شرکت
    name = models.CharField(
        max_length=255, 
        unique=True, 
        verbose_name="نام شرکت"  # نام شرکت
    )
    slug = models.SlugField(
        max_length=255, 
        unique=True, 
        blank=True, 
        verbose_name="اسلاگ"  # اسلاگ شرکت برای URL
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="توضیحات"  # توضیحات درباره شرکت
    )
    website = models.URLField(
        blank=True, 
        null=True, 
        verbose_name="وبسایت"  # لینک وبسایت شرکت
    )
    email = models.EmailField(
        blank=True, 
        null=True, 
        verbose_name="ایمیل"  # ایمیل رسمی شرکت
    )
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name="شماره تماس"  # شماره تماس
    )

    # فایل‌های رسانه‌ای شرکت
    logo = models.ImageField(
        upload_to='company/logos/', 
        blank=True, 
        null=True, 
        verbose_name="لوگو"  # لوگوی شرکت
    )
    banner = models.ImageField(
        upload_to='company/banners/', 
        blank=True, 
        null=True, 
        verbose_name="بنر"  # بنر شرکت
    )
    intro_video = models.FileField(
        upload_to='company/videos/', 
        blank=True, 
        null=True, 
        verbose_name="ویدئوی معرفی"  # ویدئو معرفی شرکت
    )

    # آدرس شرکت
    address = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="آدرس"  # آدرس کامل شرکت
    )

    location = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        max_length=100,
        verbose_name="شهر"  # شهر
    )

    postal_code = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name="کد پستی"  # کد پستی
    )

    # اطلاعات اضافی شرکت
    founded_date = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="تاریخ تأسیس"  # تاریخ تاسیس شرکت
    )
    industry = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="صنعت"  # صنعت مربوطه (مانند فناوری، سلامت)
    )
    number_of_employees = models.IntegerField(
        blank=True, 
        null=True, 
        verbose_name="تعداد کارکنان"  # تعداد کارکنان
    )

    # لینک‌های شبکه‌های اجتماعی
    linkedin = models.URLField(
        blank=True, 
        null=True, 
        verbose_name="لینک LinkedIn"  # لینک صفحه LinkedIn
    )
    twitter = models.URLField(
        blank=True, 
        null=True, 
        verbose_name="لینک Twitter"  # لینک صفحه Twitter
    )
    instagram = models.URLField(
        blank=True, 
        null=True, 
        verbose_name="لینک Instagram"  # لینک صفحه Instagram
    )

    # زمان‌بندی‌ها
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="تاریخ ایجاد"  # تاریخ ایجاد رکورد
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="تاریخ بروزرسانی"  # تاریخ آخرین به‌روزرسانی رکورد
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        قبل از ذخیره‌سازی، اسلاگ را بر اساس نام شرکت تنظیم می‌کند.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)
