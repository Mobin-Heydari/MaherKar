from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل کاربر
    """

    class Meta:
        # مدل مربوطه
        model = User

        # فیلدهایی که سریالایز می‌شوند
        fields = [
            'id',  # شناسه یکتا
            'username',  # نام کاربری
            'email',  # ایمیل
            'phone',  # شماره تلفن
            'user_type',  # نوع کاربر
            'tfa_status',  # وضعیت احراز هویت دو مرحله‌ای
            'status',  # وضعیت حساب
            'joined_date',  # تاریخ عضویت
            'password',  # رمز عبور
        ]

        # فیلدهای فقط خواندنی (مثلاً تاریخ عضویت)
        read_only_fields = ['joined_date']
