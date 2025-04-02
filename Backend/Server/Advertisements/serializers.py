from django.utils.text import slugify

from rest_framework import serializers
from .models import JobAdvertisement, Application, ResumeAdvertisement
from Companies.models import Company
from Companies.serializers import CompanySerializer
from Users.serializers import UserSerializer
from Industry.serializers import IndustrySerializer
from Locations.serializers import CitySerializer
from Locations.models import City  # used for lookup

from Profiles.serializers import JobSeekerProfileSerializer  # Serializer for JobSeekerProfile
from Resumes.serializers import JobSeekerResumeSerializer   # Serializer for JobSeekerResume



class ApplicationSerializer(serializers.ModelSerializer):
    # Nested serializers for related fields
    job_seeker = JobSeekerProfileSerializer(read_only=True)  # Display job seeker profile details
    resume = JobSeekerResumeSerializer(read_only=True)  # Display resume details

    status_display = serializers.ReadOnlyField(source='get_status_display')  # Display verbose status

    class Meta:
        model = Application
        fields = [
            'id', 'job_seeker', 'advertisement', 'cover_letter', 'resume',
            'status', 'status_display', 'employer_notes', 'viewed_by_employer',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'job_seeker', 'advertisement', 'resume', 'status', 'status_display',
            'viewed_by_employer', 'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        # Automatically set the job_seeker from the authenticated user
        request = self.context.get("request")
        validated_data['job_seeker'] = request.user.profile  # Assuming JobSeekerProfile is linked to User
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Forbid updates to critical fields
        forbidden_fields = ["job_seeker", "advertisement", "resume"]
        for field in forbidden_fields:
            if field in validated_data:
                raise serializers.ValidationError({field: f"You cannot change the {field} field."})
        
        # Allow updates for other allowed fields
        return super().update(instance, validated_data)

