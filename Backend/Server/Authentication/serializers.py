from django.utils.crypto import get_random_string  # ایمپورت برای تولید رشته تصادفی برای توکن‌ها
from rest_framework import serializers  # سریالایزرهای جنگو REST framework برای تعریف و مدیریت داده‌ها
from rest_framework import validators  # ولیداتورهای استاندارد برای اعتبارسنجی داده‌ها

from rest_framework_simplejwt.tokens import RefreshToken  # ایمپورت برای تولید توکن‌های JWT

from Users.models import User  # مدل کاربر از برنامه Users
from .models import OneTimePassword, UserRegisterOTP  # مدل‌های رمز یکبار مصرف

from random import randint  # ایمپورت کتابخانه random برای تولید اعداد تصادفی





# تعریف سریالایزر برای ورود کاربران
class LoginSerializer(serializers.Serializer):
    """
    سریالایزر برای اعتبارسنجی شماره تلفن و رمز عبور.
    """

    phone = serializers.CharField(max_length=255)  # فیلد شماره تلفن
    
    password = serializers.CharField(max_length=255, write_only=True)  # فیلد رمز عبور با قابلیت نوشتن فقط


    def validate_phone(self, value):  # متد اعتبارسنجی فیلد شماره تلفن

        if not User.objects.filter(phone=value).exists():  # بررسی وجود شماره تلفن در دیتابیس
            raise serializers.ValidationError('شماره تلفن موجود نیست')  # خطا اگر شماره یافت نشود
        return value  # بازگرداندن شماره تلفن معتبر


    def validate_password(self, value):  # متد اعتبارسنجی رمز عبور

        if len(value) < 8:  # بررسی طول رمز عبور (حداقل 8 کاراکتر)
            raise serializers.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد')  # خطای طول رمز عبور
        return value  # بازگرداندن رمز عبور معتبر


    def validate(self, data):  # متد کلی برای اعتبارسنجی داده‌های ورودی

        phone = data.get('phone')  # دریافت شماره تلفن

        password = data.get('password')  # دریافت رمز عبور

        if phone is None or password is None:  # بررسی پر بودن مقادیر
            raise serializers.ValidationError('شماره تلفن و رمز عبور هر دو الزامی هستند')  # خطای عدم مقدار
        
        user = User.objects.get(phone=phone)  # دریافت کاربر از دیتابیس
        
        if not user.check_password(password):  # بررسی صحت رمز عبور
            raise serializers.ValidationError('رمز عبور اشتباه است')  # خطا برای رمز نادرست
        return data  # بازگرداندن داده‌های معتبر



# سریالایزر برای مدیریت رمز یکبار مصرف
class OneTimePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = OneTimePassword
        fields = "__all__"

    
    def create(self, validated_data):  # متد ایجاد رمز یکبار مصرف
        code = randint(100000, 999999)  # تولید کد تصادفی ۶ رقمی
        token = get_random_string(100)  # تولید توکن طولانی تصادفی
        otp = OneTimePassword.objects.create(  # ایجاد شیء جدید رمز یکبار مصرف
            phone=validated_data['phone'],
            token=token,
            code=code
        )
        otp.save()  # ذخیره در دیتابیس
        otp.get_expiration()  # تنظیم زمان انقضا
        return {'token': token, 'code': code}  # بازگشت توکن و کد



# سریالایزر برای ثبت نام با رمز یکبار مصرف
class UserRegisterOneTimePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRegisterOTP  # اتصال سریالایزر به مدل UserRegisterOTP
        fields = "__all__"  # استفاده از تمام فیلدها در سریالایزر
        read_only_fields = ['otp']


    def create(self, validated_data):  # متد ایجاد کاربر

        code = randint(100000, 999999)  # تولید کد ۶ رقمی

        token = get_random_string(100)  # تولید توکن تصادفی

        otp = OneTimePassword.objects.create(  # ایجاد رمز یکبار مصرف
            token=token,
            code=code
        )

        otp.save()  # ذخیره در دیتابیس

        otp.get_expiration()  # تنظیم زمان انقضا

        user_register_otp = UserRegisterOTP.objects.create(  # ایجاد رکورد ثبت‌نام
            otp=otp,
            email=validated_data['email'],
            phone=validated_data['phone'],
            username=validated_data['username'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            password_conf=validated_data['password_conf']
        )

        user_register_otp.save()  # ذخیره رکورد ثبت‌نام

        return {'phone': user_register_otp.phone, 'token': token, 'code': code}  # بازگشت داده‌ها



# سریالایزر برای تایید ثبت‌نام کاربران با رمز یکبار مصرف
class UserRegisterSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6, required=True)  # فیلد کد رمز

    def validate(self, attrs):  # متد اعتبارسنجی داده‌ها

        otp_token = self.context.get('otp_token')  # دریافت توکن از کانتکست

        otp = OneTimePassword.objects.get(token=otp_token)  # دریافت رمز از دیتابیس

        if otp.status_validation() == 'ACT':  # بررسی فعال بودن رمز

            if otp.code == attrs['code']:  # تطبیق کد ورودی با کد ذخیره شده

                return attrs  # بازگشت داده‌های معتبر
            
            else:
                raise serializers.ValidationError({'code': 'Invalid OTP code.'})  # خطا برای کد اشتباه
        else:
            raise serializers.ValidationError('Inactive OTP')  # خطا برای رمز غیرفعال


    def create(self, validated_data, token):  # متد ایجاد کاربر نهایی

        otp = OneTimePassword.objects.get(token=token)  # دریافت رمز یکبار مصرف

        user_register_otp = otp.registration_otps  # ارتباط با رکورد ثبت‌نام

        user = User.objects.create_user(  # ایجاد کاربر
            email=user_register_otp.email,
            phone=user_register_otp.phone,
            username=user_register_otp.username,
            password=user_register_otp.password,
            full_name=user_register_otp.full_name,
            user_type=user_register_otp.user_type
        )

        user.save()  # ذخیره کاربر در دیتابیس

        refresh = RefreshToken.for_user(user)  # تولید توکن برای کاربر

        return {
            'user': {  # بازگشت اطلاعات کاربر
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'user_type': user.user_type
            },
            'tokens': {  # بازگشت توکن‌ها
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }
