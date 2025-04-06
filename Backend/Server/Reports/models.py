from django.db import models
from Users.models import User
from Advertisements.models import Advertisement
from Profiles.models import AdminProfile, SupportProfile, EmployerProfile, JobSeekerProfile


class ReportCategory(models.Model):
    """
    Represents categories for reports (e.g., spam, harassment).
    """
    name = models.CharField(
        unique=True,
        max_length=50,
        verbose_name="نام دسته‌بندی گزارش"
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات دسته‌بندی"
    )

    def __str__(self):
        return self.name


class JobSeekerReport(models.Model):
    """
    Model for reporting JobSeekers.
    """
    class ReportStatus(models.TextChoices):
        PENDING = "P", "در انتظار"
        RESOLVED = "R", "حل شده"
        REJECTED = "RJ", "رد شده"

    status = models.CharField(
        max_length=2,
        choices=ReportStatus.choices,
        default=ReportStatus.PENDING,
        verbose_name="وضعیت گزارش"
    )

    reported_jobseeker = models.ForeignKey(
        JobSeekerProfile,
        on_delete=models.CASCADE,
        verbose_name="جوینده کار گزارش شده",
        related_name="jobseeker_reports_against",
    )

    reporter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="jobseeker_reports",
        verbose_name="گزارش‌دهنده"
    )

    category = models.ForeignKey(
        ReportCategory, on_delete=models.CASCADE, verbose_name="دسته‌بندی گزارش"
    )

    description = models.TextField(blank=True, verbose_name="توضیحات گزارش")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")

    def __str__(self):
        return f"Report against JobSeeker: {self.reported_jobseeker.username}"


class EmployerReport(models.Model):
    """
    Model for reporting Employers.
    """

    class ReportStatus(models.TextChoices):
        PENDING = "P", "در انتظار"
        RESOLVED = "R", "حل شده"
        REJECTED = "RJ", "رد شده"

    status = models.CharField(
        max_length=2,
        choices=ReportStatus.choices,
        default=ReportStatus.PENDING,
        verbose_name="وضعیت گزارش"
    )

    reported_employer = models.ForeignKey(
        EmployerProfile,
        on_delete=models.CASCADE,
        related_name="employer_reports_against",
        verbose_name="کارفرمای گزارش شده"
    )

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="employer_reports",
        verbose_name="گزارش‌ دهنده"
    )

    category = models.ForeignKey(
        ReportCategory,
        on_delete=models.CASCADE,
        verbose_name="دسته‌بندی گزارش"
    )

    description = models.TextField(blank=True, verbose_name="توضیحات گزارش")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")

    def __str__(self):
        return f"Report against Employer: {self.reported_employer.username}"



class AdvertisementReport(models.Model):
    """
    Model for reporting advertisements.
    """

    class ReportStatus(models.TextChoices):
        PENDING = "P", "در انتظار"
        RESOLVED = "R", "حل شده"
        REJECTED = "RJ", "رد شده"

    status = models.CharField(
        max_length=2,
        choices=ReportStatus.choices,
        default=ReportStatus.PENDING,
        verbose_name="وضعیت گزارش"
    )

    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name="reports_against_joqb_advertisement",
        verbose_name="آگهی گزارش شده"
    )

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="advertisement_reports",
        verbose_name="گزارش‌دهنده"
    )

    category = models.ForeignKey(
        ReportCategory,
        on_delete=models.CASCADE,
        verbose_name="دسته‌بندی گزارش"
    )

    description = models.TextField(blank=True, verbose_name="توضیحات گزارش")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")

    def __str__(self):
        return f"Report for Advertisement ID: {self.advertisement.id}"