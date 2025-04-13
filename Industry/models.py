from django.db import models  # وارد کردن ماژول مدل‌های Django جهت تعریف مدل‌های دیتابیس
from django.utils.text import slugify  # وارد کردن تابع slugify جهت تبدیل رشته به اسلاگ URL-friendly



# ------------------------------------------------------
# مدل دسته‌بندی صنایع (IndustryCategory)
# ------------------------------------------------------
class IndustryCategory(models.Model):
    """
    مدل برای دسته‌بندی صنایع.
    این مدل شامل نام دسته‌بندی، اسلاگ و آیکون مربوطه است.
    """
    name = models.CharField(
        max_length=100,         # حداکثر تعداد کاراکتر: 100
        unique=True,            # یکتایی: نام هر دسته‌بندی باید یکتا باشد
        verbose_name="نام دسته‌بندی"  # نام نمایشی فیلد در پنل ادمین
    )

    slug = models.SlugField(
        max_length=100,         # حداکثر تعداد کاراکتر: 100
        unique=True,            # یکتایی: اسلاگ باید یکتا باشد
        blank=True,             # اجازه می‌دهد این فیلد خالی بماند (در متد save پر می‌شود)
        verbose_name="اسلاگ دسته‌بندی"  # عنوان نمایشی فیلد
    )

    icon = models.ImageField(
        upload_to='Industry/categories-icon/',  # مسیر آپلود تصاویر آیکون برای دسته‌بندی‌ها
        null=True,              # در دیتابیس اجازه ذخیره مقدار None را می‌دهد
        blank=True,             # در فرم‌ها اجازه خالی بودن فیلد را فراهم می‌کند
        verbose_name="آیکون",   # عنوان نمایشی فیلد
    )

    class Meta:
        verbose_name = "دسته‌بندی"          # نام مفرد مدل جهت نمایش در پنل ادمین
        verbose_name_plural = "دسته‌بندی‌ها"  # نام جمع مدل
        ordering = ['name']                  # ترتیب نمایش بر اساس نام

    def save(self, *args, **kwargs):
        """
        در متد save اگر اسلاگ وجود نداشته باشد، آن را با استفاده از تابع slugify از نام دسته‌بندی تولید می‌کند.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)  # فراخوانی متد save والد برای ذخیره‌سازی رکورد

    def __str__(self):
        return self.name  # بازگرداندن نام دسته‌بندی به عنوان نمایش (repr) نمونه


# ------------------------------------------------------
# مدل صنایع (Industry)
# ------------------------------------------------------
class Industry(models.Model):
    """
    مدل صنایع.
    این مدل شامل نام صنعت، اسلاگ، دسته‌بندی مربوطه، آیکون و... می‌باشد.
    """
    name = models.CharField(
        max_length=100,         # حداکثر 100 کاراکتر
        unique=True,            # نام هر صنعت باید یکتا باشد
        verbose_name="نام صنعت" # عنوان نمایشی فیلد
    )

    slug = models.SlugField(
        max_length=100,         # حداکثر تعداد کاراکتر: 100
        unique=True,            # هر اسلاگ باید یکتا باشد
        blank=True,             # اگر اسلاگ تعیین نشده باشد، در متد save تولید می‌شود
        verbose_name="اسلاگ صنعت"  # عنوان نمایشی فیلد
    )
    
    category = models.ForeignKey(
        IndustryCategory,       # ارتباط به مدل دسته‌بندی صنایع
        on_delete=models.CASCADE,  # در صورت حذف دسته‌بندی، تمامی صنایع مرتبط حذف می‌شوند
        related_name="industries", # نام رابطه معکوس جهت دسترسی به صنایع یک دسته‌بندی
        verbose_name="دسته‌بندی"   # عنوان نمایشی فیلد
    )

    icon = models.ImageField(
        upload_to='Industry/industries-icon/',  # مسیر ذخیره آیکون صنایع
        null=True,              # امکان ذخیره مقدار None
        blank=True,             # فیلد اختیاری
        verbose_name="آیکون",   # عنوان نمایشی فیلد
    )

    class Meta:
        verbose_name = "صنعت"         # نام مفرد مدل جهت نمایش در پنل ادمین
        verbose_name_plural = "صنایع"  # نام جمع مدل
        ordering = ['name']           # ترتیب بر اساس نام صنعت

    def save(self, *args, **kwargs):
        """
        در متد save اگر اسلاگ صنعت مشخص نشده باشد، به صورت خودکار از نام صنعت تولید می‌شود.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)  # فراخوانی متد ذخیره والد

    def __str__(self):
        return self.name  # بازگرداندن نام صنعت برای نمایش نمونه


# ------------------------------------------------------
# مدل مهارت (Skill)
# ------------------------------------------------------
class Skill(models.Model):
    """
    مدل مهارت برای ذخیره مهارت‌های حرفه‌ای.
    این مهارت‌ها تنها توسط مدیر سیستم ایجاد و ویرایش می‌شوند؛
    جویندگان کار از مهارت‌های موجود استفاده می‌کنند.
    """
    name = models.CharField(
        max_length=100,         # محدودیت 100 کاراکتر
        unique=True,            # نام هر مهارت باید یکتا باشد
        verbose_name="نام"       # عنوان نمایشی فیلد
    )

    icon = models.ImageField(
        upload_to='Industry/skills-icons/',  # مسیر آپلود آیکون‌های مهارت
        null=True,              # فیلد اختیاری؛ امکان ذخیره مقدار None
        blank=True,             # امکان خالی بودن فیلد در فرم‌ها
        verbose_name="آیکون",   # عنوان نمایشی فیلد
    )

    industry = models.ForeignKey(
        Industry,               # ارتباط به مدل Industry؛ هر مهارت به یک صنعت مرتبط است
        on_delete=models.CASCADE,  # در صورت حذف صنعت، مهارت‌های مرتبط حذف می‌شوند
        verbose_name="صنعت",    # عنوان نمایشی فیلد
    )

    class Meta:
        verbose_name = "مهارت"             # نام مفرد مدل جهت نمایش در پنل
        verbose_name_plural = "مهارت‌ها"    # نام جمع مدل
        ordering = ['name']                # ترتیب بر اساس نام مهارت

    def __str__(self):
        return self.name  # بازگرداندن نام مهارت جهت نمایش نمونه
