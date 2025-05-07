from django.utils.crypto import get_random_string  # برای تولید رشته‌های تصادفی جهت استفاده به عنوان توکن
from rest_framework import serializers              # وارد کردن سریالایزرهای DRF برای تعریف و مدیریت داده‌ها
from rest_framework import validators               # وارد کردن ولیداتورهای استاندارد جهت اعتبارسنجی داده‌ها

from rest_framework_simplejwt.tokens import RefreshToken  # برای تولید توکن‌های JWT جهت احراز هویت

from Users.models import User, IdCardInFormation  # ایمپورت مدل‌های کاربر و اطلاعات کارت شناسایی از اپ Users
from .models import OneTimePassword, UserRegisterOTP, UserLoginOTP  # ایمپورت مدل‌های OTP و ثبت‌نام کاربر با OTP

from random import randint  # برای تولید اعداد تصادفی (به عنوان کدهای OTP)


# ========================================================
# سریالایزر ورود کاربران (LoginSerializer)
# ========================================================
class PasswordLoginSerializer(serializers.Serializer):
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

    # تعریف فیلد نام کامل
    full_name = serializers.CharField(
        required=True,  # نام کامل الزامی است
        help_text="نام کامل خود را وارد کنید"  # متن راهنما برای فیلد نام کامل
    )

    user_type = serializers.CharField(required=True, write_only=True)  # تعریف فیلد نوع کاربر

    phone = serializers.CharField(
        validators=[
            validators.UniqueValidator(queryset=User.objects.all())  # Ensure phone is unique in User model
        ],
        required=True,  # phone is required
        help_text="Enter a unique phone",  # Help text for the phone field
    )


    class Meta:
        model = UserRegisterOTP
        fields = "__all__"  
        # شامل تمام فیلدهای مدل UserRegisterOTP
        read_only_fields = ['otp']  
        # فیلد otp به صورت فقط خواندنی است؛ در زمان ثبت نام به صورت خودکار پر می‌شود


    # اعتبارسنجی فیلد نام کامل
    def validate_full_name(self, value):
        # بررسی می‌کند آیا طول نام کامل در محدوده مجاز (3-50 کاراکتر) قرار دارد
        if len(value) < 3 or len(value) > 50:
            raise serializers.ValidationError('نام کامل باید بین 3 تا 50 کاراکتر باشد')
        return value

    def validate_user_type(self, value):
        if len(value) != 2:
            raise serializers.ValidationError("نوع کاربر باید دقیقاً 2 کاراکتر طول داشته باشد.")
        if value not in ('EM', 'JS'):
            raise serializers.ValidationError("نوع کاربر باید یکی از موارد زیر باشد: EM, JS.")
        return value



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
            phone=validated_data['phone'],
            full_name=validated_data['full_name'],
            user_type=validated_data['user_type']
        )

        user_register_otp.save()

        return {'phone': user_register_otp.phone, 'token': token, 'code': code}


# ========================================================
# سریالایزر تایید ثبت‌نام کاربران با OTP (UserRegisterValidateOneTimePasswordSerializer)
# ========================================================
class UserRegisterValidateOneTimePasswordSerializer(serializers.Serializer):

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

        password = get_random_string(length=16)

        user = User.objects.create_user(
            phone=user_register_otp.phone,
            password=password,
            full_name=user_register_otp.full_name,
            user_type=user_register_otp.user_type
        )

        user.id_card_info = id_card_info

        user.save()

        refresh = RefreshToken.for_user(user)
        
        return {
            'user': {
                'phone': user.phone,
                'user_type': user.user_type,
                'password': password
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }
    

# ----------------------------------------------------------------
# سریالایزر ورود کاربر با OTP (UserLoginOneTimePasswordSerializer)
# ----------------------------------------------------------------
class UserLoginOneTimePasswordSerializer(serializers.Serializer):

    # تعریف فیلد شماره تلفن که اجباری و فقط جهت ارسال داده است (write_only)
    phone = serializers.CharField(required=True, write_only=True)

    def validate_phone(self, value):
        """
        اعتبارسنجی فیلد تلفن:
          - اطمینان حاصل می‌کند که شماره تلفن ارائه شده مقدار None نباشد.
        """
        # اگر مقدار شماره تلفن None باشد، خطای اعتبارسنجی صادر می‌شود
        if value is None:
            raise serializers.ValidationError('شماره تلفن الزامی است')
        # در صورت معتبر بودن، مقدار شماره تلفن برگردانده می‌شود
        return value

    def validate(self, atters):
        """
        اعتبارسنجی کلی داده‌های ورودی:
          - بررسی می‌کند که شماره تلفن وارد شده در پایگاه داده موجود باشد.
        """
        # بررسی می‌کنیم که آیا کاربری با شماره تلفن وارد شده در دیتابیس موجود است یا خیر
        if User.objects.filter(phone=atters['phone']).exists():
            # در صورت وجود، داده‌های معتبر برگردانده می‌شوند
            return atters
        else:
            # در غیر این صورت، پیام خطا صادر می‌شود
            raise serializers.ValidationError('شماره تلفن موجود نیست')

    def create(self, validated_data):
        # تولید یک کد تصادفی 6 رقمی برای OTP
        code = randint(100000, 999999)
        # تولید یک رشته تصادفی به عنوان توکن OTP با طول 100 کاراکتر
        token = get_random_string(100)
        
        # ایجاد رکورد جدید OTP در دیتابیس با استفاده از توکن و کد تولید شده
        otp = OneTimePassword.objects.create(
            token=token,
            code=code
        )
        # ذخیره‌سازی اطلاعات OTP در دیتابیس (گرچه create به‌طور خودکار ذخیره می‌کند)
        otp.save()
        # فراخوانی متد get_expiration جهت تعیین زمان انقضای OTP
        otp.get_expiration()
        
        # واکشی کاربر مربوط به شماره تلفن وارد شده
        user = User.objects.get(phone=validated_data['phone'])
        
        # ایجاد رکورد جدید ورود با OTP برای کاربر جهت ثبت‌سازی عملیات ورود
        user_login_otp = UserLoginOTP.objects.create(
            otp=otp,
            user=user,
            phone=validated_data['phone']
        )
        # ذخیره‌سازی اطلاعات مربوط به ورود OTP
        user_login_otp.save()

        # برگرداندن اطلاعات مورد نیاز شامل شماره تلفن، توکن OTP و کد OTP
        return {'phone': user_login_otp.phone, 'token': token, 'code': code}



# ----------------------------------------------------------------
# سریالایزر تایید ورود با OTP (UserLoginValidateOneTimePasswordSerializer)
# ----------------------------------------------------------------
class UserLoginValidateOneTimePasswordSerializer(serializers.Serializer):

    # تعریف فیلد کد OTP با محدودیت دقیقا 6 کاراکتر (min_length و max_length برابر 6)
    code = serializers.CharField(max_length=6, min_length=6, required=True)

    def validate(self, attrs):
        # بازیابی توکن OTP از context که توسط ویو ارسال شده است
        otp_token = self.context.get('otp_token')
        
        # واکشی شیء OTP مرتبط با توکن دریافتی؛ اگر OTP با توکن داده‌شده وجود نداشته باشد، خطا صادر می‌شود
        otp = OneTimePassword.objects.get(token=otp_token)

        # بررسی وضعیت اعتبار OTP؛ در صورتی که OTP فعال (ACT) باشد، ادامه ارزیابی انجام می‌شود
        if otp.status_validation() == 'ACT':
            # مطابقت کد وارد شده توسط کاربر با کد ذخیره شده در OTP
            if otp.code == attrs['code']:
                # در صورت تطابق، داده‌های ورودی به عنوان نتایج معتبر برگردانده می‌شود
                return attrs
            else:
                # در غیر این صورت، خطای اعتبارسنجی مربوط به فیلد "code" صادر می‌شود
                raise serializers.ValidationError({'code': 'Invalid OTP code.'})
        else:
            # اگر OTP به عنوان غیر فعال شناخته شود، پیام خطا ارسال می‌شود
            raise serializers.ValidationError('Inactive OTP')
