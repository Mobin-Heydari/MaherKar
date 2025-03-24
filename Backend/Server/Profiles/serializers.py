from rest_framework import serializers
from .models import JobSeekerProfile, EmployerProfile, AdminProfile, SupportProfile






class JobSeekerProfileSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل پروفایل جوینده کار.
    این سریالایزر شامل فیلدهای اصلی، مهارت‌ها، تجربیات کاری و تحصیلات می‌باشد.
    """

    class Meta:
        model = JobSeekerProfile
        fields = [
            'id',
            'user',
            'headline',
            'bio',
            'profile_picture',
            'location',
            'industry',
            'contact_email',
            'contact_phone',
            'website',
            'linkedin_profile',
            'resume',
            'job_type_preference',
            'expected_salary',
            'id_card',
            'id_card_status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']



class EmployerProfileSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل پروفایل کارفرما.
    این سریالایزر اطلاعات شرکت و تماس کارفرما را برمی‌گرداند.
    """
    class Meta:
        model = EmployerProfile
        fields = [
            'id',
            'user',
            'company_name',
            'company_logo',
            'website',
            'industry',
            'company_size',
            'description',
            'location',
            'contact_email',
            'contact_phone',
            'established_date',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']



class AdminProfileSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل پروفایل مدیر.
    این سریالایزر اطلاعات مدیریتی مانند یادداشت‌ها و سطح مدیر را نمایش می‌دهد.
    """
    class Meta:
        model = AdminProfile
        fields = [
            'id',
            'user',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']



class SupportProfileSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل پروفایل پشتیبان.
    این سریالایزر اطلاعات تخصص، ساعات کاری و امتیاز پشتیبان را برمی‌گرداند.
    """
    class Meta:
        model = SupportProfile
        fields = [
            'id',
            'user',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
