from django.db import models
from django.utils.text import slugify  # برای ایجاد اسلاگ از نام‌ها

class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)  # نام استان
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # اسلاگ مربوط به استان

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        قبل از ذخیره‌سازی، فیلد اسلاگ را بر اساس نام استان تنظیم می‌کند.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super(Province, self).save(*args, **kwargs)


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)  # ارتباط شهر با استان
    name = models.CharField(max_length=100, unique=True)  # نام شهر
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # اسلاگ مربوط به شهر

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        قبل از ذخیره‌سازی، فیلد اسلاگ را بر اساس نام شهر تنظیم می‌کند.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)
