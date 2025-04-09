from django.utils.crypto import get_random_string  # برای تولید رشته‌های تصادفی جهت استفاده به عنوان توکن
from rest_framework import serializers              # وارد کردن سریالایزرهای DRF برای تعریف و مدیریت داده‌ها
from rest_framework import validators               # وارد کردن ولیداتورهای استاندارد جهت اعتبارسنجی داده‌ها

from rest_framework_simplejwt.tokens import RefreshToken  # برای تولید توکن‌های JWT جهت احراز هویت

from Users.models import User, IdCardInFormation  # ایمپورت مدل‌های کاربر و اطلاعات کارت شناسایی از اپ Users
from .models import OneTimePassword, UserRegisterOTP  # ایمپورت مدل‌های OTP و ثبت‌نام کاربر با OTP

from random import randint  # برای تولید اعداد تصادفی (به عنوان کدهای OTP)


# ========================================================
# سریالایزر ورود کاربران (LoginSerializer)
# ========================================================
class LoginSerializer(serializers.Serializer):
    """
    سریالایزر برای اعتبارسنجی شماره تلفن و رمز عبور هنگام ورود.
    """
    phone = serializers.CharField(max_length=255)  
    # فیلد شماره تلفن؛ ورودی کاربر برای شناسایی وی
    password = serializers.CharField(max_length=255, write_only=True)  
    # فیلد رمز عبور؛ با حالت write_only که هنگام خروجی برگردانده نمی‌شود

    def validate_phone(self, value):
        """
        اعتبارسنجی فیلد تلفن:
          - بررسی می‌کند که آیا شماره تلفن در دیتابیس موجود است یا خیر.
        """
        if not User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('شماره تلفن موجود نیست')
        return value

    def validate_password(self, value):
        """
        اعتبارسنجی فیلد رمز عبور:
          - بررسی می‌کند که طول رمز عبور حداقل ۸ کاراکتر باشد.
        """
        if len(value) < 8:
            raise serializers.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد')
        return value

    def validate(self, data):
        """
        اعتبارسنجی کلی داده‌های ورودی:
          - چک می‌کند که شماره تلفن و رمز عبور وجود داشته باشند.
          - کاربر مربوط به شماره تلفن را واکشی می‌کند و صحت رمز عبور را بررسی می‌کند.
        """
        phone = data.get('phone')
        password = data.get('password')
        if phone is None or password is None:
            raise serializers.ValidationError('شماره تلفن و رمز عبور هر دو الزامی هستند')
        user = User.objects.get(phone=phone)
        if not user.check_password(password):
            raise serializers.ValidationError('رمز عبور اشتباه است')
        return data


# ========================================================
# سریالایزر رمز یکبار مصرف (OneTimePasswordSerializer)
# ========================================================
class OneTimePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneTimePassword
        fields = "__all__"  
        # استفاده از تمام فیلدهای مدل OneTimePassword

    def create(self, validated_data):
        """
        متد ایجاد OTP:
          - یک کد تصادفی ۶ رقمی تولید می‌کند.
          - توکن طولانی تصادفی نیز تولید می‌کند.
          - یک نمونه جدید OneTimePassword با استفاده از شماره تلفن موجود در validated_data ایجاد می‌شود.
          - زمان انقضا با فراخوانی متد get_expiration تنظیم می‌شود.
          - در نهایت توکن و کد تولید شده برگردانده می‌شود.
        """
        code = randint(100000, 999999)
        token = get_random_string(100)
        otp = OneTimePassword.objects.create(
            phone=validated_data['phone'],
            token=token,
            code=code
        )
        otp.save()
        otp.get_expiration()
        return {'token': token, 'code': code}


# ========================================================
# سریالایزر ثبت نام کاربران با OTP (UserRegisterOneTimePasswordSerializer)
# ========================================================
class UserRegisterOneTimePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegisterOTP
        fields = "__all__"  
        # شامل تمام فیلدهای مدل UserRegisterOTP
        read_only_fields = ['otp']  
        # فیلد otp به صورت فقط خواندنی است؛ در زمان ثبت نام به صورت خودکار پر می‌شود

    def create(self, validated_data):
        """
        متد ایجاد ثبت‌نام کاربر با OTP:
          - ابتدا یک کد ۶ رقمی و یک توکن تصادفی تولید می‌کند.
          - یک نمونه جدید OneTimePassword ایجاد می‌شود و زمان انقضا تنظیم می‌شود.
          - سپس رکورد ثبت‌نام کاربر (UserRegisterOTP) با استفاده از داده‌های ورودی و OTP ایجاد می‌شود.
          - در نهایت شماره تلفن، توکن و کد تولید شده برگردانده می‌شود.
        """
        code = randint(100000, 999999)
        token = get_random_string(100)
        otp = OneTimePassword.objects.create(
            token=token,
            code=code
        )
        otp.save()
        otp.get_expiration()
        user_register_otp = UserRegisterOTP.objects.create(
            otp=otp,
            email=validated_data['email'],
            phone=validated_data['phone'],
            username=validated_data['username'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            password_conf=validated_data['password_conf']
        )
        user_register_otp.save()
        return {'phone': user_register_otp.phone, 'token': token, 'code': code}


# ========================================================
# سریالایزر تایید ثبت‌نام کاربران با OTP (UserRegisterSerializer)
# ========================================================
class UserRegisterSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6, required=True)  
    # فیلد کد OTP؛ باید دقیقا ۶ کاراکتر باشد

    def validate(self, attrs):
        """
        اعتبارسنجی OTP:
          - توکن OTP از context دریافت می‌شود.
          - OTP مربوطه را از دیتابیس واکشی می‌کند.
          - ابتدا وضعیت OTP بررسی می‌شود؛ اگر فعال باشد، سپس کد ورودی با کد ذخیره شده تطبیق داده می‌شود.
          - در صورت ناهماهنگی، خطای اعتبارسنجی صادر می‌شود.
        """
        otp_token = self.context.get('otp_token')
        otp = OneTimePassword.objects.get(token=otp_token)
        if otp.status_validation() == 'ACT':
            if otp.code == attrs['code']:
                return attrs
            else:
                raise serializers.ValidationError({'code': 'Invalid OTP code.'})
        else:
            raise serializers.ValidationError('Inactive OTP')

    def create(self, validated_data, token):
        """
        متد ایجاد نهایی کاربر پس از تایید OTP:
          - OTP مورد نظر با استفاده از توکن دریافت می‌شود.
          - رکورد ثبت‌نام کاربر (UserRegisterOTP) از طریق رابطه معکوس otp.registration_otps دریافت می‌شود.
          - یک نمونه IdCardInFormation نیز ایجاد می‌شود (به عنوان مثال جهت ثبت اطلاعات شناسایی کاربر).
          - سپس کاربر جدید با استفاده از متد create_user ساخته می‌شود.
          - توکن‌های JWT (refresh و access) برای کاربر تولید شده و اطلاعات کاربر به همراه توکن‌ها برگردانده می‌شود.
        """
        otp = OneTimePassword.objects.get(token=token)
        user_register_otp = otp.registration_otps  # دریافت رکورد ثبت‌نام مرتبط با OTP
        id_card_info = IdCardInFormation.objects.create()
        user = User.objects.create_user(
            email=user_register_otp.email,
            phone=user_register_otp.phone,
            username=user_register_otp.username,
            password=user_register_otp.password,
            full_name=user_register_otp.full_name,
            user_type=user_register_otp.user_type
        )
        user.id_card_info = id_card_info
        user.save()
        refresh = RefreshToken.for_user(user)
        return {
            'user': {
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'user_type': user.user_type
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }
