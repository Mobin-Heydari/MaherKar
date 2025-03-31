from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SubscriptionPlan(models.Model):
    """
    Represents a subscription plan (e.g., Basic, Premium).
    """
    name = models.CharField(max_length=100, verbose_name="Plan Name", unique=True)

    description = models.TextField(blank=True, verbose_name="Description")

    price_per_day = models.BigIntegerField(verbose_name="Price per Day")

    active = models.BooleanField(default=True, verbose_name="Active")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    def __str__(self):
        return self.name


class Duration(models.Model):
    """
    Represents the duration of a subscription plan.
    """
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name="durations",
        verbose_name="Plan"
    )
    day = models.IntegerField(default=30, verbose_name="Days")

    class Meta:
        verbose_name = "Duration"
        verbose_name_plural = "Durations"
    
    def __str__(self):
        return f"{self.day} Days for {self.plan.name}"


class JobAdvertisementSubscription(models.Model):
    """
    Subscription linked to a JobAdvertisement model instance.
    """
    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', "Pending"
        ACTIVE = 'active', "Active"
        EXPIRED = 'expired', "Expired"
        CANCELED = 'canceled', "Canceled"
        FAILED = 'failed', "Failed"


    advertisement = models.ForeignKey(
        'Advertisement.JobAdvertisement',
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Job Advertisement"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="User"
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Plan"
    )

    duration = models.ForeignKey(
        Duration,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Duration"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name="Payment Status"
    )

    start_date = models.DateTimeField(default=timezone.now, verbose_name="Start Date")

    end_date = models.DateTimeField(verbose_name="End Date")

    last_payment_date = models.DateTimeField(null=True, blank=True, verbose_name="Last Payment Date")
    next_payment_date = models.DateTimeField(null=True, blank=True, verbose_name="Next Payment Date")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        abstract = True

    def is_active(self):
        """
        Check if the subscription is active based on payment status and expiration date.
        """
        return self.payment_status == self.PaymentStatus.ACTIVE and timezone.now() < self.end_date
    
    def __str__(self):
        return f"Job Ad Subscription for {self.advertisement.title}"


class JobseekerResumeAdvertisementSubscription(models.Model):
    """
    Subscription linked to a JobseekerResumeAdvertisement model instance.
    """

    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', "Pending"
        ACTIVE = 'active', "Active"
        EXPIRED = 'expired', "Expired"
        CANCELED = 'canceled', "Canceled"
        FAILED = 'failed', "Failed"


    advertisement = models.ForeignKey(
        'Advertisement.JobseekerResumeAdvertisement',
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Job Seeker Advertisement"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="User"
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Plan"
    )

    duration = models.ForeignKey(
        Duration,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Duration"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name="Payment Status"
    )

    start_date = models.DateTimeField(default=timezone.now, verbose_name="Start Date")

    end_date = models.DateTimeField(verbose_name="End Date")

    last_payment_date = models.DateTimeField(null=True, blank=True, verbose_name="Last Payment Date")
    next_payment_date = models.DateTimeField(null=True, blank=True, verbose_name="Next Payment Date")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        abstract = True

    def is_active(self):
        """
        Check if the subscription is active based on payment status and expiration date.
        """
        return self.payment_status == self.PaymentStatus.ACTIVE and timezone.now() < self.end_date
    
    def __str__(self):
        return f"Job Seeker Ad Subscription for {self.advertisement.title}"
