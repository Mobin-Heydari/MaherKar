from django.contrib.auth.models import BaseUserManager




class UserManager(BaseUserManager):
    """
        کلاسی برای مدیریت کاربران و ایجاد آن‌ها
    """

    # متد ایجاد یک کاربر عادی
    def create_user(self, phone, username, email, user_type, password=None): 
        """
        کاربری با مشخصات داده‌شده ایجاد و بازمی‌گرداند.
        """

        # بررسی اینکه ایمیل وارد شده است
        if not email:
            raise ValueError("ایمیل باید وارد شود")  # ایمیل الزامی است

        # بررسی اینکه نام کاربری وارد شده است
        if not username:
            raise ValueError("نام کاربری باید وارد شود")  # نام کاربری الزامی است

        # بررسی اینکه شماره تلفن وارد شده است
        if not phone:
            raise ValueError("شماره تلفن باید وارد شود")  # شماره تلفن الزامی است
        
        # نرمال کردن (تبدیل به حروف کوچک) ایمیل وارد شده
        email = self.normalize_email(email)
        
        # ایجاد نمونه‌ای از مدل کاربر
        user = self.model(
            phone=phone,  # شماره تلفن کاربر
            username=username,  # نام کاربری
            email=email,  # ایمیل
            user_type=user_type,  # نوع کاربر (نقش)
        )
        
        # تنظیم رمز عبور
        user.set_password(password)  # هش کردن و تنظیم رمز عبور
        user.save(using=self._db)  # ذخیره کاربر در پایگاه داده

        return user 

    # متد ایجاد ادمین
    def create_superuser(self, phone, username, email, password=None):
        """
        ادمین با مشخصات داده‌شده ایجاد و بازمی‌گرداند.
        """
        
        # استفاده از متد ایجاد کاربر برای ایجاد ادمین
        user = self.create_user(
            phone=phone,  # شماره تلفن ادمین
            email=self.normalize_email(email),  # ایمیل نرمال شده
            username=username,  # نام کاربری
            user_type="AD",  # ادمین ها همیشه باید نقش مدیر داشته باشند
            password=password,  # رمز عبور
        )
        
        # تنظیم دسترسی‌های مدیریت و ادمین
        user.is_admin = True  # تنظیم به عنوان مدیر
        user.is_superuser = True  # تنظیم به عنوان ادمین
        user.save(using=self._db)  # ذخیره تغییرات در پایگاه داده
        
        return user
