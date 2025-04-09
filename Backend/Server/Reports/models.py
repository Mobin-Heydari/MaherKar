from django.db import models  
# ایمپورت مدل‌های Django جهت تعریف مدل‌های دیتابیس

from Users.models import User  
# ایمپورت مدل User از اپ کاربران جهت ثبت گزارش‌دهنده‌ها

from Advertisements.models import Advertisement  
# ایمپورت مدل Advertisement از اپ آگهی‌ها جهت ثبت گزارش‌های مربوط به آگهی‌ها

from Profiles.models import EmployerProfile, JobSeekerProfile  
# ایمپورت مدل‌های پروفایل کارفرما و جوینده کار جهت ثبت گزارش‌های مربوط به کاربران


# =============================================================================
# مدل ReportCategory (دسته‌بندی گزارش‌ها)
# =============================================================================
class ReportCategory(models.Model):
    """
    مدل دسته‌بندی گزارش‌ها، مانند: اسپم، آزار و اذیت.
    """

    # نام دسته‌بندی گزارش؛ یکتا و محدود به 50 کاراکتر
    name = models.CharField(
        unique=True,
        max_length=50,
        verbose_name="نام دسته‌بندی گزارش"
    )

    # توضیحات مربوط به دسته‌بندی گزارش؛ امکان خالی بودن فراهم است
    description = models.TextField(
        blank=True,
        verbose_name="توضیحات دسته‌بندی"
    )

    def __str__(self):
        # نمایش نام دسته‌بندی در خروجی نمایشی مدل
        return self.name


# =============================================================================
# مدل JobSeekerReport (گزارش جویندگان کار)
# =============================================================================
class JobSeekerReport(models.Model):
    """
    مدل مربوط به گزارش‌های مرتبط با جویندگان کار.
    """

    class ReportStatus(models.TextChoices):
        PENDING = "P", "در انتظار"  # وضعیت گزارش: در انتظار بررسی
        RESOLVED = "R", "حل شده"     # وضعیت گزارش: بررسی و حل شده
        REJECTED = "RJ", "رد شده"    # وضعیت گزارش: رد شده

    # وضعیت گزارش؛ انتخاب از میان گزینه‌های ReportStatus
    status = models.CharField(
        max_length=2,
        choices=ReportStatus.choices,
        default=ReportStatus.PENDING,
        verbose_name="وضعیت گزارش"
    )

    # جوینده کار گزارش شده؛ ارتباط با مدل JobSeekerProfile
    reported_jobseeker = models.ForeignKey(
        JobSeekerProfile,
        on_delete=models.CASCADE,  # در صورت حذف جوینده کار، گزارش نیز حذف می‌شود
        verbose_name="جوینده کار گزارش شده",
        related_name="jobseeker_reports_against"
    )

    # کاربری که گزارش را ثبت کرده است؛ ارتباط با مدل User
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # در صورت حذف گزارش‌دهنده، گزارش نیز حذف می‌شود
        related_name="jobseeker_reports",
        verbose_name="گزارش‌دهنده"
    )

    # دسته‌بندی گزارش؛ ارتباط با مدل ReportCategory
    category = models.ForeignKey(
        ReportCategory,
        on_delete=models.CASCADE,  # در صورت حذف دسته‌بندی، گزارش نیز حذف می‌شود
        verbose_name="دسته‌بندی گزارش"
    )

    # توضیحات گزارش؛ امکان خالی بودن فراهم است
    description = models.TextField(blank=True, verbose_name="توضیحات گزارش")

    # زمان ایجاد گزارش؛ به صورت خودکار ثبت می‌شود
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")

    def __str__(self):
        # نمایش نام جوینده کار گزارش شده در خروجی نمایشی مدل
        return f"Report against JobSeeker: {self.reported_jobseeker.username}"


# =============================================================================
# مدل EmployerReport (گزارش کارفرماها)
# =============================================================================
class EmployerReport(models.Model):
    """
    مدل مربوط به گزارش‌های مرتبط با کارفرماها.
    """

    class ReportStatus(models.TextChoices):
        PENDING = "P", "در انتظار"
        RESOLVED = "R", "حل شده"
        REJECTED = "RJ", "رد شده"

    # وضعیت گزارش؛ انتخاب از میان گزینه‌های ReportStatus
    status = models.CharField(
        max_length=2,
        choices=ReportStatus.choices,
        default=ReportStatus.PENDING,
        verbose_name="وضعیت گزارش"
    )

    # کارفرمای گزارش شده؛ ارتباط با مدل EmployerProfile
    reported_employer = models.ForeignKey(
        EmployerProfile,
        on_delete=models.CASCADE,  # در صورت حذف کارفرما، گزارش نیز حذف می‌شود
        related_name="employer_reports_against",
        verbose_name="کارفرمای گزارش شده"
    )

    # کاربری که گزارش را ثبت کرده است؛ ارتباط با مدل User
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # در صورت حذف گزارش‌دهنده، گزارش نیز حذف می‌شود
        related_name="employer_reports",
        verbose_name="گزارش‌ دهنده"
    )

    # دسته‌بندی گزارش؛ ارتباط با مدل ReportCategory
    category = models.ForeignKey(
        ReportCategory,
        on_delete=models.CASCADE,  # در صورت حذف دسته‌بندی، گزارش نیز حذف می‌شود
        verbose_name="دسته‌بندی گزارش"
    )

    # توضیحات گزارش؛ امکان خالی بودن فراهم است
    description = models.TextField(blank=True, verbose_name="توضیحات گزارش")

    # زمان ایجاد گزارش؛ به صورت خودکار ثبت می‌شود
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")

    def __str__(self):
        # نمایش نام کارفرما گزارش شده در خروجی نمایشی مدل
        return f"Report against Employer: {self.reported_employer.username}"


# =============================================================================
# مدل AdvertisementReport (گزارش آگهی‌ها)
# =============================================================================
class AdvertisementReport(models.Model):
    """
    مدل مربوط به گزارش‌های مرتبط با آگهی‌ها.
    """

    class ReportStatus(models.TextChoices):
        PENDING = "P", "در انتظار"
        RESOLVED = "R", "حل شده"
        REJECTED = "RJ", "رد شده"

    # وضعیت گزارش؛ انتخاب از میان گزینه‌های ReportStatus
    status = models.CharField(
        max_length=2,
        choices=ReportStatus.choices,
        default=ReportStatus.PENDING,
        verbose_name="وضعیت گزارش"
    )

    # آگهی گزارش شده؛ ارتباط با مدل Advertisement
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,  # در صورت حذف آگهی، گزارش نیز حذف می‌شود
        related_name="reports_against_joqb_advertisement",
        verbose_name="آگهی گزارش شده"
    )

    # کاربری که گزارش را ثبت کرده است؛ ارتباط با مدل User
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # در صورت حذف گزارش‌دهنده، گزارش نیز حذف می‌شود
        related_name="advertisement_reports",
        verbose_name="گزارش‌دهنده"
    )

    # دسته‌بندی گزارش؛ ارتباط با مدل ReportCategory
    category = models.ForeignKey(
        ReportCategory,
        on_delete=models.CASCADE,  # در صورت حذف دسته‌بندی، گزارش نیز حذف می‌شود
        verbose_name="دسته‌بندی گزارش"
    )

    # توضیحات گزارش؛ امکان خالی بودن فراهم است
    description = models.TextField(blank=True, verbose_name="توضیحات گزارش")

    # زمان ایجاد گزارش؛ به صورت خودکار ثبت می‌شود
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")

    def __str__(self):
        # نمایش شناسه آگهی گزارش شده در خروجی نمایشی مدل
        return f"Report for Advertisement ID: {self.advertisement.id}"
