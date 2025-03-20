from rest_framework import serializers
from .models import (
    JobSeekerProfile, Experience, Education,
    SkillCategory, Skill,
    EmployerProfile, AdminProfile, SupportProfile
)


class SkillCategorySerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل دسته‌بندی مهارت.
    این سریالایزر اطلاعاتی مانند نام، اسلاگ و آیکون دسته‌بندی مهارت را برمی‌گرداند.
    """
    class Meta:
        model = SkillCategory
        fields = ['id', 'name', 'slug', 'icon']
        read_only_fields = ['slug']  # اسلاگ به صورت خودکار تولید می‌شود



class SkillSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل مهارت.
    در این سریالایزر، دسته‌بندی مهارت به صورت تو در تو (nested) نمایش داده می‌شود.
    """
    category = SkillCategorySerializer(read_only=True)

    class Meta:
        model = Skill
        fields = ['id', 'name', 'description', 'icon', 'website', 'category']



class ExperienceSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل تجربه کاری.
    این سریالایزر اطلاعات مربوط به هر تجربه کاری جوینده کار را برمی‌گرداند.
    """
    class Meta:
        model = Experience
        fields = ['id', 'title', 'company', 'location', 'start_date', 'end_date', 'description']



class EducationSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل تحصیلات.
    این سریالایزر تمام اطلاعات مربوط به تحصیلات یک جوینده کار را نمایش می‌دهد.
    """
    class Meta:
        model = Education
        fields = ['id', 'school', 'degree', 'field_of_study', 'start_date', 'end_date', 'description']



class JobSeekerProfileSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل پروفایل جوینده کار.
    این سریالایزر شامل فیلدهای اصلی، مهارت‌ها، تجربیات کاری و تحصیلات می‌باشد.
    """
    # نمایش مهارت‌ها به صورت تو در تو؛ تنها خواندنی می‌باشد
    skills = SkillSerializer(many=True, read_only=True)
    # نمایش تجربیات کاری به صورت تو در تو؛ تنها خواندنی می‌باشد
    experiences = ExperienceSerializer(many=True, read_only=True)
    # نمایش تحصیلات به صورت تو در تو؛ تنها خواندنی می‌باشد
    educations = EducationSerializer(many=True, read_only=True)

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
            'skills',
            'created_at',
            'updated_at',
            'experiences',
            'educations'
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
            'notes',
            'admin_level',
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
            'expertise_area',
            'work_hours',
            'rating',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
