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
    Serializer for personal information.
    """
    class Meta:
        model = PersonalInformation
        fields = ['gender', 'age', 'kids_count']
        # Remove read_only_fields if you want to allow updates
        # read_only_fields = []


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Job Seeker Profile model.
    """
    # Remove read_only=True so that this nested field can also accept input data.
    personal_info = PersonalInformationSerializer()

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
        # Pop the nested data out of the parent data.
        personal_info_data = validated_data.pop('personal_info', None)
        
        # Update the main JobSeekerProfile fields.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
    
        # If there is nested personal information, update it.
        if personal_info_data:
            # Here we assume that instance.personal_info exists.
            personal_info_instance = instance.personal_info
            # You can either update each field manually:
            for attr, value in personal_info_data.items():
                setattr(personal_info_instance, attr, value)
            personal_info_instance.save()
            
            # --- OR, alternatively, you can delegate to the nested serializer's update() method:
            # serializer = PersonalInformationSerializer(personal_info_instance, data=personal_info_data, partial=True)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
    
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
        # Pop the nested data out of the parent data.
        personal_info_data = validated_data.pop('personal_info', None)
        
        # Update the main JobSeekerProfile fields.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
    
        # If there is nested personal information, update it.
        if personal_info_data:
            # Here we assume that instance.personal_info exists.
            personal_info_instance = instance.personal_info
            # You can either update each field manually:
            for attr, value in personal_info_data.items():
                setattr(personal_info_instance, attr, value)
            personal_info_instance.save()
            
            # --- OR, alternatively, you can delegate to the nested serializer's update() method:
            # serializer = PersonalInformationSerializer(personal_info_instance, data=personal_info_data, partial=True)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
    
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