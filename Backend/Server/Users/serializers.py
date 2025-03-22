from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل کاربر
    """

    class Meta:
        model = User
        fields = [
            'id',                        # شناسه یکتا
            'username',                  # نام کاربری
            'full_name',                 # نام و نام خانوادگی
            'email',                     # ایمیل
            'phone',                     # شماره تلفن
            'user_type',                 # نوع کاربر
            'two_factor_auth_status',    # وضعیت احراز هویت دو مرحله‌ای
            'tfa_verified_at',           # زمان تایید احراز هویت دو مرحله‌ای
            'status',                    # وضعیت حساب کاربری
            'email_verified',            # وضعیت تایید ایمیل
            'phone_verified',            # وضعیت تایید شماره تلفن
            'joined_date',               # تاریخ عضویت
            'last_updated',              # تاریخ آخرین به‌روزرسانی حساب
            'password',                  # رمز عبور
        ]
        read_only_fields = ['id', 'joined_date', 'last_updated', 'tfa_verified_at']
        extra_kwargs = {
            'password': {'write_only': True},
        }