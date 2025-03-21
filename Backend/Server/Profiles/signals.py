from django.db.models.signals import post_save
from django.dispatch import receiver
from Users.models import User
from Profiles.models import JobSeekerProfile, EmployerProfile, AdminProfile, SupportProfile





@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    ایجاد پروفایل برای کاربر بر اساس user_type در زمان ایجاد کاربر.
    """
    if created:
        if instance.user_type == "JS":  # Job Seeker
            JobSeekerProfile.objects.create(
                user=instance,
                gender="M",  # مقدار پیش‌فرض
                location="Undefined",  # مقدار پیش‌فرض
            )
        elif instance.user_type == "EM":  # Employer
            EmployerProfile.objects.create(
                user=instance,
                company_name="Undefined",  # مقدار پیش‌فرض
                location="Undefined",  # مقدار پیش‌فرض
            )
        elif instance.user_type == "AD":  # Admin
            AdminProfile.objects.create(user=instance)
        elif instance.user_type == "SU":  # Support
            SupportProfile.objects.create(user=instance)
