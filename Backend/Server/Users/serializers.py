from rest_framework import serializers
from .models import User, IdCardInformation



class IdCardInformationSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای اطلاعات کارت ملی
    """

    class Meta:
        model = IdCardInformation
        fields = "__all__"

    def update(self, instance, validated_data):
        request = self.context.get('request')

        if request.user.is_staff:
            instance.id_card_status == validated_data.get('id_card_status', instance.id_card_status)

        instance.id_card == validated_data.get('id_card', instance.id_card)
        instance.id_card_number == validated_data.get('id_card_number', instance.id_card_number)

        instance.save()
        return instance




class UserSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل کاربر
    """

    id_card_info = IdCardInformationSerializer()

    class Meta:
        model = User
        fields = [
            'id',                        # شناسه یکتا
            'id_card_info',
            'username',                  # نام کاربری
            'full_name',                 # نام و نام خانوادگی
            'email',                     # ایمیل
            'phone',                     # شماره تلفن
            'user_type',                 # نوع کاربر
            'status',                    # وضعیت حساب کاربری
            'joined_date',               # تاریخ عضویت
            'last_updated',              # تاریخ آخرین به‌روزرسانی حساب
            'password',                  # رمز عبور
        ]
        read_only_fields = ['id', 'joined_date', 'last_updated', 'id_card_info']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)