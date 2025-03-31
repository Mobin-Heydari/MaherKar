from django.db import models
from Users.models import User
from Advertisements.models import JobAdvertisement, JobseekerResumeAdvertisement
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



class AdminReport(models.Model):
    """
    Model for reporting Admins.
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

    reported_admin = models.ForeignKey(
        AdminProfile,
        on_delete=models.CASCADE,
        related_name="admin_reports_against",
        verbose_name="مدیر گزارش شده"
    )

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="admin_reports",
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
        return f"Report against Admin: {self.reported_admin.username}"


class SupportReport(models.Model):
    """
    Model for reporting Support users.
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

    reported_support = models.ForeignKey(
        SupportProfile,
        on_delete=models.CASCADE,
        related_name="support_reports_against",
        verbose_name="پشتیبان گزارش شده"
    )

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="support_reports",
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
        return f"Report against Support: {self.reported_support.username}"


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

    job_advertisement = models.ForeignKey(
        JobAdvertisement,
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


class ResumeReport(models.Model):
    """
    Model for reporting resumes.
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

    resume_advertisement = models.ForeignKey(
        JobseekerResumeAdvertisement,
        on_delete=models.CASCADE,
        related_name="reports_against_resume_advertisement",
        verbose_name="رزومه گزارش شده"
    )

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="resume_reports",
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
        return f"Report for Resume ID: {self.resume.id}"
