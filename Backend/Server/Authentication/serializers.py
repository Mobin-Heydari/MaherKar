from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework import validators

from rest_framework_simplejwt.tokens import RefreshToken

from Users.models import User
from .models import OneTimePassword

from random import randint



# تعریف کلاس LoginSerializer
class LoginSerializer(serializers.Serializer):
    """
    سریالایزر برای اعتبارسنجی شماره تلفن و رمز عبور.
    """
    # تعریف فیلد شماره تلفن
    phone = serializers.CharField(max_length=255)
    
    # تعریف فیلد رمز عبور
    password = serializers.CharField(max_length=255, write_only=True)

    # اعتبارسنجی فیلد شماره تلفن
    def validate_phone(self, value):
        # بررسی وجود شماره تلفن در دیتابیس
        if not User.objects.filter(phone=value).exists():
            # پرتاب خطای اعتبارسنجی در صورت عدم وجود شماره تلفن
            raise serializers.ValidationError('شماره تلفن موجود نیست')
        # بازگشت شماره تلفن اعتبارسنجی شده
        return value

    # اعتبارسنجی فیلد رمز عبور
    def validate_password(self, value):
        # بررسی طول رمز عبور که حداقل ۸ کاراکتر باشد
        if len(value) < 8:
            # پرتاب خطای اعتبارسنجی در صورت کوتاه بودن رمز عبور
            raise serializers.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد')
        # بازگشت رمز عبور اعتبارسنجی شده
        return value

    # اعتبارسنجی کل سریالایزر
    def validate(self, data):
        # دریافت شماره تلفن و رمز عبور از داده‌ها
        phone = data.get('phone')
        password = data.get('password')
        
        # بررسی ارائه شدن شماره تلفن و رمز عبور
        if phone is None or password is None:
            # پرتاب خطای اعتبارسنجی در صورت نبود شماره تلفن یا رمز عبور
            raise serializers.ValidationError('شماره تلفن و رمز عبور هر دو الزامی هستند')
        
        # دریافت شیء کاربر از دیتابیس
        user = User.objects.get(phone=phone)
        
        # بررسی صحت رمز عبور
        if not user.check_password(password):
            # پرتاب خطای اعتبارسنجی در صورت نادرست بودن رمز عبور
            raise serializers.ValidationError('رمز عبور اشتباه است')
        
        # بازگشت داده‌های اعتبارسنجی شده
        return data




# سریالایزر برای مدیریت رمز یکبار مصرف
class OneTimePasswordSerializer(serializers.Serializer):
    
    # فیلد شماره تلفن با ولیداتور برای اطمینان از عدم استفاده تکراری شماره تلفن
    phone = serializers.CharField(
        max_length=15,
        validators=[
            validators.UniqueValidator(queryset=User.objects.all())  # بررسی منحصر به فرد بودن شماره تلفن در بین کاربران
        ]
    )
    
    # متدی برای ایجاد رکورد جدید رمز یکبار مصرف
    def create(self, validated_data):
        """
        ایجاد رمز یکبار مصرف جدید با داده‌های اعتبارسنجی شده.
        
        :param validated_data: داده‌های تاییدشده
        :return: یک دیکشنری شامل توکن و کد رمز یکبار مصرف
        """
        
        # تولید کد تصادفی ۶ رقمی برای رمز یکبار مصرف
        code = randint(100000, 999999)  # تولید کد ۶ رقمی
        # تولید توکن تصادفی طولانی
        token = get_random_string(100)  # تولید توکن با طول ۱۰۰ کاراکتر
        
        # ایجاد یک رکورد جدید از مدل رمز یکبار مصرف با استفاده از داده‌های تاییدشده
        otp = OneTimePassword.objects.create(
            phone=validated_data['phone'],  # ذخیره شماره تلفن کاربر
            token=token,  # ذخیره توکن
            code=code  # ذخیره کد
        )
        
        # ذخیره شیء رمز یکبار مصرف در دیتابیس
        otp.save()
        
        # تنظیم زمان انقضای رمز یکبار مصرف
        otp.get_expiration()  # فراخوانی متد زمان انقضا از مدل
        
        # بازگشت داده‌های رمز یکبار مصرف
        return {
            'token': token,  # توکن رمز یکبار مصرف
            'code': code  # کد رمز یکبار مصرف
        }


