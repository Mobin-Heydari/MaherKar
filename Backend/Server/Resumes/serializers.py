from rest_framework import serializers
from .models import JobSeekerResume, Experience, Education, JobSeekerSkill
from Industry.serializers import IndustrySerializer, SkillSerializer
from Locations.serializers import CitySerializer




# Nested serializer for Experience
class ExperienceSerializer(serializers.ModelSerializer):
    # Nest the City (location) representation
    location = CitySerializer(read_only=True)
    # Optionally, you can also add a read-only field for employment_type's display value if desired:
    employment_type_display = serializers.ReadOnlyField(source='get_employment_type_display')
    
    class Meta:
        model = Experience
        fields = [
            'id',
            'employment_type', 
            'employment_type_display',
            'title',
            'company',
            'location',
            'start_date',
            'end_date',
            'description'
        ]


# Nested serializer for Education
class EducationSerializer(serializers.ModelSerializer):
    # You can include read-only display values for degree as well if you want:
    class Meta:
        model = Education
        fields = [
            'id',
            'school',
            'degree',
            'grade',
            'field_of_study',
            'start_date',
            'end_date',
            'description'
        ]


# Nested serializer for JobSeekerSkill
class JobSeekerSkillSerializer(serializers.ModelSerializer):
    # Use nested Skill representation.
    skill = SkillSerializer(read_only=True)
    level_display = serializers.ReadOnlyField(source='get_level_display')
    
    class Meta:
        model = JobSeekerSkill
        fields = [
            'id',
            'skill',
            'level',
            'level_display'
        ]


# Main serializer for JobSeekerResume
class JobSeekerResumeSerializer(serializers.ModelSerializer):
    # If desired, you may nest the job_seeker_profile details using its appropriate serializer.
    # For now, we include it as a primary key.
    job_seeker_profile = serializers.PrimaryKeyRelatedField(read_only=True)
    
    industry = IndustrySerializer(read_only=True)
    location = CitySerializer(read_only=True)
    
    # Nested relationships (using the related_name defined in your models)
    experiences = ExperienceSerializer(many=True, read_only=True, source='Experiences')
    educations = EducationSerializer(many=True, read_only=True, source='Educations')
    skills = JobSeekerSkillSerializer(many=True, read_only=True, source='Job_Seeker_Skills')
    
    # Optionally, include display values for choice fields
    gender_display = serializers.ReadOnlyField(source='get_gender_display')
    soldier_status_display = serializers.ReadOnlyField(source='get_soldier_status_display')
    degree_display = serializers.ReadOnlyField(source='get_degree_display')
    expected_salary_display = serializers.ReadOnlyField(source='get_expected_salary_display')
    experience_choice_display = serializers.ReadOnlyField(source='get_experience_display')
    preferred_job_type_display = serializers.ReadOnlyField(source='get_preferred_job_type_display')
    availability_display = serializers.ReadOnlyField(source='get_availability_display')
    
    class Meta:
        model = JobSeekerResume
        fields = [
            'id',
            'job_seeker_profile',
            'industry',
            'headline',
            'bio',
            'website',
            'linkedin_profile',
            'location',
            'gender',
            'gender_display',
            'soldier_status',
            'soldier_status_display',
            'degree',
            'degree_display',
            'years_of_experience',
            'experience',  # This is the choice field (e.g. 'No EXPERIENCE', etc.)
            'experience_choice_display',
            'expected_salary',
            'expected_salary_display',
            'preferred_job_type',
            'preferred_job_type_display',
            'cv',
            'availability',
            'availability_display',
            'created_at',
            'updated_at',
            'experiences',
            'educations',
            'skills',
        ]
