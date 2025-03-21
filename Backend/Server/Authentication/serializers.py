from rest_framework import serializers
from rest_framework import validators

from rest_framework_simplejwt.tokens import RefreshToken

from Users.models import User



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
