from django.db import models
from django.utils.text import slugify  # برای ایجاد اسلاگ از نام‌ها




class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)  # نام استان

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)  # ارتباط شهر با استان
    name = models.CharField(max_length=100)  # نام شهر

    def __str__(self):
        return self.name
