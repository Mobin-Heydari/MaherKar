from django.db import models         # وارد کردن ماژول مدل‌های Django جهت تعریف کلاس‌های مدل
from django.utils.text import slugify  # وارد کردن تابع slugify برای تبدیل رشته‌ها به اسلاگ (URL-friendly)



# -------------------------------------------------------
# مدل استان (Province)
# -------------------------------------------------------
class Province(models.Model):
    # فیلد name: نام استان، به‌گونه‌ای که یکتا باشد (هیچ استان با نام تکراری وجود نداشته باشد)
    name = models.CharField(max_length=100, unique=True)  # نام استان

    # فیلد slug: رشته‌ای URL-friendly به‌طور خودکار از نام استان ایجاد می‌شود؛ یکتا بوده و می‌تواند خالی گذاشته شود
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # unique slug for province

    def save(self, *args, **kwargs):
        """
        در متد save:
        - در صورتی که فیلد slug تعریف نشده باشد، آن را از طریق تابع slugify و براساس مقدار فیلد name تولید می‌کند.
        """
        if not self.slug:
            self.slug = slugify(self.name)  # تبدیل نام استان به اسلاگ
        super().save(*args, **kwargs)  # فراخوانی متد save کلاس والد جهت ذخیره‌سازی در دیتابیس

    def __str__(self):
        # نمایش نام استان به عنوان نمایش نمونه (نمایش خواندنی در پنل ادمین و سایر بخش‌ها)
        return self.name


# -------------------------------------------------------
# مدل شهر (City)
# -------------------------------------------------------
class City(models.Model):
    # فیلد province: ارتباط شهر با یک استان از طریق یک کلید خارجی (ForeignKey)
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE  # در صورت حذف یک استان، تمامی شهرهای مرتبط نیز حذف می‌شوند
    )  # ارتباط شهر با استان

    # فیلد name: نام شهر، مانند استان محدود به 100 کاراکتر است
    name = models.CharField(max_length=100)  # نام شهر

    # فیلد slug: رشته‌ای URL-friendly که در صورتی که ارائه نشود، به طور خودکار از نام شهر تولید می‌شود؛ باید یکتا باشد
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # unique slug for city

    def save(self, *args, **kwargs):
        """
        در متد save:
        - اگر فیلد slug برای شهر خالی باشد، از نام شهر به‌صورت خودکار اسلاگ تولید می‌شود.
        """
        if not self.slug:
            self.slug = slugify(self.name)  # تولید اسلاگ از نام شهر
        super().save(*args, **kwargs)  # ذخیره اطلاعات شهر در دیتابیس

    def __str__(self):
        # بازگرداندن نام شهر به عنوان نمایش نمونه
        return self.name
