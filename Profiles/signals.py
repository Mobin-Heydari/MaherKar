from django.db.models.signals import post_save        # ایمپورت سیگنال post_save جهت دریافت پیام پس از ذخیره یک شیء
from django.dispatch import receiver                    # ایمپورت دکوریتور receiver برای اتصال تابع به سیگنال مربوطه
from Users.models import User                           # ایمپورت مدل کاربر از اپلیکیشن Users
from Profiles.models import (                           # ایمپورت مدل‌های پروفایل و اطلاعات شخصی از اپلیکیشن Profiles
    JobSeekerProfile,
    EmployerProfile,
    AdminProfile,
    SupportProfile,
    PersonalInformation
)


# اتصال سیگنال post_save به مدل User جهت ایجاد خودکار پروفایل‌های مربوطه پس از ایجاد یک کاربر جدید
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    این سیگنال پس از ذخیره یک شیء از مدل User اجرا می‌شود.
    در صورتی که کاربر تازه ایجاد شده باشد (created=True)، بر اساس نوع کاربر،
    پروفایل مربوطه (جوینده‌کار، کارفرما، مدیر یا پشتیبان) به همراه اطلاعات شخصی پیش‌فرض ایجاد می‌شود.
    """
    if created:  # بررسی اینکه آیا شیء User جدید ایجاد شده است یا خیر
        if instance.user_type == "JS":  # در صورتی که نوع کاربر "جوینده کار" باشد
            # ایجاد اطلاعات شخصی با مقدار پیش‌فرض؛ می‌توانید مقدارها را در صورت نیاز تغییر دهید.
            personal_info = PersonalInformation.objects.create(
                gender=PersonalInformation.Gender.MAN,   # تعیین جنسیت پیش‌فرض به عنوان "آقا"
                age=18                                     # تعیین سن پیش‌فرض: 18 سال
            )
            # ایجاد پروفایل جوینده کار با استفاده از اطلاعات کاربر و اطلاعات شخصی ایجاد شده
            JobSeekerProfile.objects.create(
                user=instance,            # اتصال پروفایل به کاربر ایجاد شده
                personal_info=personal_info,  # اتصال اطلاعات شخصی به پروفایل
                headline="Undefined",     # عنوان شغلی پیش‌فرض؛ قابل تغییر توسط کاربر در آینده
                bio="",                   # بیوگرافی پیش‌فرض خالی
                profile_picture=None,     # پیش‌فرض تصویر پروفایل تعیین نشده
                location=None,            # پیش‌فرض شهر (در صورت تمایل می‌توانید به یک شهر پیش‌فرض اشاره کنید)
                industry=None,            # پیش‌فرض صنعت نامشخص
            )
        elif instance.user_type == "EM":  # در صورتی که نوع کاربر "کارفرما" باشد
            # ایجاد اطلاعات شخصی با مقادیر پیش‌فرض؛ مقدار سن برای کارفرمایان معمولاً بالاتر است.
            personal_info = PersonalInformation.objects.create(
                gender=PersonalInformation.Gender.MAN,   # جنسیت پیش‌فرض "آقا"؛ در صورت نیاز تغییر یابد
                age=30                                     # سن پیش‌فرض تعیین شده برای کارفرما: 30 سال
            )
            # ایجاد پروفایل کارفرما با استفاده از اطلاعات شخصی و سایر فیلدهای پیش‌فرض
            EmployerProfile.objects.create(
                user=instance,            # اتصال پروفایل به کاربر ایجاد شده
                company_name="Undefined", # نام شرکت پیش‌فرض؛ کارفرمایان باید در آینده آن را به‌روز کنند
                personal_info=personal_info,
                bio="",                   # بیوگرافی پیش‌فرض خالی
                profile_picture=None,     # تصویر پروفایل پیش‌فرض تعیین نشده
                location=None,            # شهر پیش‌فرض نامشخص
                industry=None,            # صنعت پیش‌فرض نامشخص
            )
        elif instance.user_type == "AD":  # در صورتی که نوع کاربر "مدیر" باشد
            # ایجاد پروفایل مدیر؛ معمولاً نیازی به اطلاعات اضافی پیچیده نیست.
            AdminProfile.objects.create(
                user=instance           # اتصال مستقیم پروفایل مدیر به کاربر ایجاد شده
            )
        elif instance.user_type == "SU":  # در صورتی که نوع کاربر "پشتیبان" باشد
            # ایجاد پروفایل پشتیبان سیستم
            SupportProfile.objects.create(
                user=instance           # اتصال پروفایل پشتیبان به کاربر ایجاد شده
            )
