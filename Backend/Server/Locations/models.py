from django.db import models
from django.utils.text import slugify




class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)  # نام استان
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # unique slug for province

    def save(self, *args, **kwargs):
        # Automatically generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)  # ارتباط شهر با استان
    name = models.CharField(max_length=100)  # نام شهر
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # unique slug for city

    def save(self, *args, **kwargs):
        # Automatically generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
