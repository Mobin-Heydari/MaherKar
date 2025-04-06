from rest_framework import serializers

from .models import Advertisement, JobAdvertisement, Application, ResumeAdvertisement

from Companies.models import Company
from Profiles.models import EmployerProfile, JobSeekerProfile
from Resumes.models import JobSeekerResume

from Companies.serializers import CompanySerializer
from Industry.serializers import IndustrySerializer
from Locations.serializers import CitySerializer
from Subscriptions.serializers import AdvertisementSubscription
from Profiles.serializers import JobSeekerProfileSerializer, EmployerProfileSerializer
from Resumes.serializers import JobSeekerResumeSerializer
from Users.serializers import UserSerializer





class AdvertisementSerializer(serializers.ModelSerializer):

    owner = UserSerializer()
    industry = IndustrySerializer()
    location = CitySerializer()
    subscription = AdvertisementSubscription()

    industry_slug = serializers.CharField()
    location_slug = serializers.CharField()



    class Meta:
        model = Advertisement
        fields = [
            'id', 'owner', 'industry', 'subscription', 'location', 'title', 'slug',
            'advertise_code', 'description', 'status', 'gender',
            'soldier_status', 'degree', 'salary', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'advertise_code', 'slug', 'created_at', 'updated_at', 'subscription', 'owner']
    

    def update(self, instance, validated_data):
        request = self.context.get('request')

        if request.user.is_staff:
            instance.status = validated_data.get("status", instance.status)
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class JobAdvertisementSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer()
    company = CompanySerializer()
    employer = EmployerProfileSerializer()


    company_slug = serializers.CharField(write_only=True)
    employer_slug = serializers.CharField(write_only=True)

    class Meta:
        model = JobAdvertisement
        fields = [
            'id', 'advertisement', 'company_slug', 'company',
            'employer', 'job_type', 'description_position'
        ]
        read_only_fields = ['id', 'company', 'employer']

    def create(self, validated_data):
        request = self.context.get('request')
        employer_profile_id = self.context.get("employer_profile_id")

        # Retrieve and validate the company
        company_slug = validated_data.pop("company_slug")
        try:
            company = Company.objects.get(slug=company_slug)
        except Company.DoesNotExist:
            raise serializers.ValidationError({"company_slug": "Company with the given slug does not exist."})

        # Retrieve and validate the employer
        try:
            employer = EmployerProfile.objects.get(id=employer_profile_id)
        except Company.DoesNotExist:
            raise serializers.ValidationError({"employer": "Employer profile with the given id does not exist."})

        # Retrieve and validate nested advertisement data
        advertisement_data = validated_data.pop("advertisement")
        advertisement = Advertisement.objects.create(
            owner=request.user,
            **advertisement_data
        )

        # Create the job advertisement
        job_advertisement = JobAdvertisement.objects.create(
            advertisement=advertisement,
            company=company,
            employer=employer,
            **validated_data
        )
        return job_advertisement
    


    def update(self, instance, validated_data):
        # Forbid updates to company or employer through this serializer
        forbidden_fields = ["company", "employer"]
        for field in forbidden_fields:
            if field in validated_data:
                raise serializers.ValidationError({field: f"You cannot update the {field} field."})

        # Update the job advertisement fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ResumeAdvertisementSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer()
    job_seeker_profile = JobSeekerProfileSerializer()
    resume = JobSeekerResumeSerializer()

    job_seeker_slug = serializers.CharField(write_only=True)
    resume_slug = serializers.CharField(write_only=True)

    class Meta:
        model = ResumeAdvertisement
        fields = [
            'id', 'advertisement', 'resume_slug', 
            'job_seeker_profile', 'resume', 'job_type'
        ]
        read_only_fields = ['id', 'job_seeker_profile', 'resume', 'advertisement']



    def create(self, validated_data):
        request = self.context.get('request')
        jobseeker_profile_id = self.context.get('jobseeker_profile_id')

        try:
            job_seeker_profile = JobSeekerProfile.objects.get(id=jobseeker_profile_id)
        except JobSeekerProfile.DoesNotExist:
            raise serializers.ValidationError({"profile": "profile with the given id does not exist."})
        
        try:
            resume = JobSeekerResume.objects.get(job_seeker_profile=job_seeker_profile)
        except JobSeekerProfile.DoesNotExist:
            raise serializers.ValidationError({"resume": "Resume with the given profile does not exist."})
        

        # Retrieve and validate nested advertisement data
        advertisement_data = validated_data.pop("advertisement")
        advertisement = Advertisement.objects.create(
            owner=request.user,
            **advertisement_data
        )

        # Create the resume advertisement
        resume_advertisement = ResumeAdvertisement.objects.create(
            advertisement=advertisement,
            job_seeker_profile=job_seeker_profile,
            resume=resume,
            **validated_data
        )
        return resume_advertisement


    def update(self, instance, validated_data):
        # Forbid updates to job seeker profile or resume through this serializer
        forbidden_fields = ["job_seeker_profile", "resume", "advertisement"]
        for field in forbidden_fields:
            if field in validated_data:
                raise serializers.ValidationError({field: f"You cannot update the {field} field."})
        
        # Update the resume advertisement fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


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

        request = self.context.get('request')
        # Forbid updates to critical fields
        forbidden_fields = ["job_seeker", "advertisement", "resume"]

        if request.user == instance.advertisement.advertisement.owner:
            instance.status = validated_data.get('status', instance.status)

        for field in forbidden_fields:
            if field in validated_data:
                raise serializers.ValidationError({field: f"You cannot change the {field} field."})
        
        instance.save()
        
        # Allow updates for other allowed fields
        return super().update(instance, validated_data)

