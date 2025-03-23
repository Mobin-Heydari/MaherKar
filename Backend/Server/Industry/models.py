from django.db import models
from django.utils.text import slugify


class IndustryCategory(models.Model):
    """
    Model for Industry Categories
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="نام دسته‌بندی"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name="اسلاگ دسته‌بندی"
    )


    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['name']


    def save(self, *args, **kwargs):
        """
        Auto-generate slug from the name if not provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name



class Industry(models.Model):
    """
    Model for Industries
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="نام صنعت"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name="اسلاگ صنعت"
    )
    category = models.ForeignKey(
        IndustryCategory,
        on_delete=models.CASCADE,
        related_name="industries",
        verbose_name="دسته‌بندی"
    )



    class Meta:
        verbose_name = "صنعت"
        verbose_name_plural = "صنایع"
        ordering = ['name']


    def save(self, *args, **kwargs):
        """
        Auto-generate slug from the name if not provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
