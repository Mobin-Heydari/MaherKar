from rest_framework import serializers
from .models import (
    PersonalInformation,
    JobSeekerProfile,
    EmployerProfile,
    AdminProfile,
    SupportProfile
)

class PersonalInformationSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای اطلاعات شخصی
    """

    class Meta:
        model = PersonalInformation
        fields = ['gender', 'age', 'kids_count']
        read_only_fields = []

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل پروفایل جوینده کار.
    """
    personal_info = PersonalInformationSerializer(read_only=True)

    class Meta:
        model = JobSeekerProfile
        fields = [
            'id',
            'user',
            'personal_info',
            'id_card_info',
            'headline',
            'bio',
            'profile_picture',
            'location',
            'industry',
            'contact_email',
            'job_type_preference',
            'expected_salary',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class EmployerProfileSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل پروفایل کارفرما.
    """
    personal_info = PersonalInformationSerializer(read_only=True)

    class Meta:
        model = EmployerProfile
        fields = [
            'id',
            'user',
            'company_name',
            'personal_info',
            'id_card_info',
            'bio',
            'profile_picture',
            'location',
            'industry',
            'contact_email',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class AdminProfileSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل پروفایل مدیر.
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