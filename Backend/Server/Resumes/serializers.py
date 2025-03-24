from rest_framework import serializers
from .models import JobSeekerResume, Experience, Education, JobSeekerSkill


# JobSeekerResume Serializer
class JobSeekerResumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobSeekerResume
        fields = [
            'id', 'job_seeker_profile', 'industry', 'headline', 'bio', 'website', 'linkedin_profile',
            'location', 'gender', 'soldier_status', 'degree', 'years_of_experience',
            'experience', 'expected_salary', 'preferred_job_type', 'cv', 'availability',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['job_seeker_profile', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        """
        Forbid updates to immutable fields like job_seeker_profile.
        """
        # Remove the job_seeker_profile from validated_data if present
        if 'job_seeker_profile' in validated_data:
            raise serializers.ValidationError({"job_seeker_profile": "You cannot update the job seeker profile."})

        # Proceed with updating other allowed fields
        return super().update(instance, validated_data)


# Experience Serializer
class ExperienceSerializer(serializers.ModelSerializer):
    resume_id = serializers.IntegerField(write_only=True)  # Accept resume ID for creation

    class Meta:
        model = Experience
        fields = [
            'id', 'resume', 'resume_id', 'employment_type', 'title', 'company', 'location',
            'start_date', 'end_date', 'description'
        ]
        read_only_fields = ['resume']

    def create(self, validated_data):
        resume_id = validated_data.pop('resume_id')
        try:
            resume = JobSeekerResume.objects.get(id=resume_id)
            validated_data['resume'] = resume
        except JobSeekerResume.DoesNotExist:
            raise serializers.ValidationError({"resume_id": "Resume with the given ID does not exist."})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Prevent updating the resume field
        validated_data.pop('resume', None)
        validated_data.pop('resume_id', None)
        return super().update(instance, validated_data)


# Education Serializer
class EducationSerializer(serializers.ModelSerializer):
    resume_id = serializers.IntegerField(write_only=True)  # Accept resume ID for creation

    class Meta:
        model = Education
        fields = [
            'id', 'resume', 'resume_id', 'school', 'degree', 'grade', 'field_of_study',
            'start_date', 'end_date', 'description'
        ]
        read_only_fields = ['resume']

    def create(self, validated_data):
        resume_id = validated_data.pop('resume_id')
        try:
            resume = JobSeekerResume.objects.get(id=resume_id)
            validated_data['resume'] = resume
        except JobSeekerResume.DoesNotExist:
            raise serializers.ValidationError({"resume_id": "Resume with the given ID does not exist."})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Prevent updating the resume field
        validated_data.pop('resume', None)
        validated_data.pop('resume_id', None)
        return super().update(instance, validated_data)


# JobSeekerSkill Serializer
class JobSeekerSkillSerializer(serializers.ModelSerializer):
    resume_id = serializers.IntegerField(write_only=True)  # Accept resume ID for creation

    class Meta:
        model = JobSeekerSkill
        fields = [
            'id', 'resume', 'resume_id', 'skill', 'level'
        ]
        read_only_fields = ['resume']

    def create(self, validated_data):
        resume_id = validated_data.pop('resume_id')
        try:
            resume = JobSeekerResume.objects.get(id=resume_id)
            validated_data['resume'] = resume
        except JobSeekerResume.DoesNotExist:
            raise serializers.ValidationError({"resume_id": "Resume with the given ID does not exist."})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Prevent updating the resume field
        validated_data.pop('resume', None)
        validated_data.pop('resume_id', None)
        return super().update(instance, validated_data)
