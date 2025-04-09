from django.db.models.signals import post_save
from django.dispatch import receiver
from Users.models import User
from Profiles.models import JobSeekerProfile, EmployerProfile, AdminProfile, SupportProfile, PersonalInformation




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "JS":  # Job Seeker
            # ایجاد اطلاعات شخصی با مقدار پیش‌فرض؛ در صورت نیاز این مقدارها را دچار تغییر کنید.
            personal_info = PersonalInformation.objects.create(
                gender=PersonalInformation.Gender.MAN,  # مقدار پیش‌فرض
                age=18  # مقدار پیش‌فرض
            )
            JobSeekerProfile.objects.create(
                user=instance,
                personal_info=personal_info,
                headline="Undefined",       # مقدار پیش‌فرض، قابل تغییر
                bio="",
                profile_picture=None,
                location=None,              # مقدار پیش‌فرض؛ می‌توانید آن را به یک City خاص تغییر دهید
                industry=None,
                website="",
                linkedin_profile="",
            )
        elif instance.user_type == "EM":  # Employer
            # ایجاد اطلاعات شخصی و کارت ملی با مقدار پیش‌فرض مناسب برای کارفرما
            personal_info = PersonalInformation.objects.create(
                gender=PersonalInformation.Gender.MAN,  # مقدار پیش‌فرض؛ تغییر در صورت نیاز
                age=30  # مقدار پیش‌فرض برای کارفرما
            )
            EmployerProfile.objects.create(
                user=instance,
                company_name="Undefined",    # مقدار پیش‌فرض؛ کارفرمایان باید بعداً آن را به‌روز کنند
                personal_info=personal_info,
                bio="",
                profile_picture=None,
                location=None,
                industry=None,
            )
        elif instance.user_type == "AD":  # Admin
            AdminProfile.objects.create(user=instance)
        elif instance.user_type == "SU":  # Support
            SupportProfile.objects.create(user=instance)
