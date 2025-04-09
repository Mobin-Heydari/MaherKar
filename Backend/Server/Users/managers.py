from django.contrib.auth.models import BaseUserManager  # وارد کردن کلاس مدیریت پایه جهت استفاده در تعریف منیجر سفارشی




# تعریف منیجر کاربر با ارث‌بری از BaseUserManager جهت مدیریت ایجاد کاربر و سوپر یوزر
class UserManager(BaseUserManager):
    """
    مدیریتی برای ایجاد کاربران و ادمین‌ها.
    """

    # متدی برای ایجاد یک کاربر معمولی با دریافت مشخصات لازم
    def create_user(self, phone, username, email, user_type, full_name, password=None, **extra_fields):
        """
        ایجاد و بازگرداندن یک کاربر معمولی با مشخصات داده‌شده.
        """
        # بررسی می‌کنیم که ایمیل ارائه شده باشد؛ در صورت عدم وجود ایمیل خطا رخ می‌دهد
        if not email:
            raise ValueError("ایمیل باید وارد شود")
        # بررسی می‌کنیم که نام کاربری ارائه شده باشد؛ در صورت عدم وجود خطا برگردانده می‌شود
        if not username:
            raise ValueError("نام کاربری باید وارد شود")
        # بررسی وجود شماره تلفن؛ در صورت خالی بودن، خطا داده می‌شود
        if not phone:
            raise ValueError("شماره تلفن باید وارد شود")
        
        # نرمال‌سازی ایمیل جهت یکسان‌سازی (معمولاً به حروف کوچک)
        email = self.normalize_email(email)
        
        # ایجاد نمونه‌ای از مدل کاربر با استفاده از مقادیر ورودی و هر فیلد اضافی در صورت نیاز
        user = self.model(
            phone=phone,         # شماره تلفن به عنوان شناسه اصلی
            username=username,   # نام کاربری یکتا
            email=email,         # ایمیل نرمال شده
            user_type=user_type, # نوع کاربر (برای مثال: جوینده کار، کارفرما، پشتیبان یا مدیر)
            full_name=full_name, # نام کامل کاربر
            **extra_fields,      # سایر فیلدهای اضافی در صورت نیاز
        )
        
        # تنظیم رمز عبور کاربر به صورت هش شده
        user.set_password(password)
        # ذخیره کاربر در دیتابیس؛ استفاده از دیتابیس پیش‌فرض یا دیتابیسی که در _db مشخص شده است
        user.save(using=self._db)
        return user  # بازگرداندن نمونه ایجاد شده کاربر

    # متدی برای ایجاد یک سوپر یوزر (ادمین) با دریافت مشخصات لازم
    def create_superuser(self, phone, username, email, full_name, password=None, **extra_fields):
        """
        ایجاد و بازگرداندن یک ادمین (سوپر یوزر) برای سیستم.
        """
        # استفاده از متد create_user برای ساختن یک کاربر؛ به جز نوع کاربر که به صورت ثابت "AD" (مدیر) تنظیم می‌شود
        user = self.create_user(
            phone=phone,
            username=username,
            email=self.normalize_email(email),  # نرمال‌سازی ایمیل قبل از ارسال
            full_name=full_name,
            password=password,
            user_type="AD"  # تنظیم نوع کاربر به "مدیر" جهت ادمین بودن
        )

        user.is_admin = True       # علامت زدن کاربر به عنوان مدیر سیستم
        user.is_superuser = True   # علامت زدن کاربر به عنوان سوپر یوزر برای دسترسی کامل

        # ذخیره مجدد تغییرات در دیتابیس
        user.save(using=self._db)

        return user  # بازگرداندن کاربر ادمین ایجاد شده
