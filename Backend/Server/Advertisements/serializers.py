from django.utils.text import slugify

from rest_framework import serializers
from .models import JobAdvertisement, Application, JobseekerResumeAdvertisement
from Companies.models import Company
from Companies.serializers import CompanySerializer
from Users.serializers import UserSerializer
from Industry.serializers import IndustrySerializer
from Locations.serializers import CitySerializer
from Locations.models import City  # used for lookup

from Profiles.serializers import JobSeekerProfileSerializer  # Serializer for JobSeekerProfile
from Resumes.serializers import JobSeekerResumeSerializer   # Serializer for JobSeekerResume



class JobAdvertisementSerializer(serializers.ModelSerializer):
    # Nested serializers for related models
    company = CompanySerializer(read_only=True)
    industry = IndustrySerializer(read_only=True)
    employer = UserSerializer(read_only=True)
    location = CitySerializer(read_only=True)  # represents location data

    # Write-only fields for passing slugs on create
    company_slug = serializers.CharField(write_only=True)
    location_slug = serializers.CharField(write_only=True)

    # Read-only display fields for choice fields
    gender_display = serializers.ReadOnlyField(source='get_gender_display')
    soldier_status_display = serializers.ReadOnlyField(source='get_soldier_status_display')
    degree_display = serializers.ReadOnlyField(source='get_degree_display')
    experience_display = serializers.ReadOnlyField(source='get_experience_display')
    salary_display = serializers.ReadOnlyField(source='get_salary_display')
    status_display = serializers.ReadOnlyField(source='get_status_display')

    class Meta:
        model = JobAdvertisement
        fields = [
            'id',
            'company',
            'company_slug',   # write-only: used for lookup
            'industry',
            'employer',
            'location',
            'location_slug',  # write-only: used for lookup
            'title',
            'slug',
            'advertise_code',
            'description_position',
            'status',
            'status_display',
            'gender',
            'gender_display',
            'soldier_status',
            'soldier_status_display',
            'degree',
            'degree_display',
            'experience',
            'experience_display',
            'salary',
            'salary_display',
            'created_at',
            'updated_at',
        ]
        # The following fields are read-only via the API
        read_only_fields = [
            'advertise_code', 
            'created_at', 
            'updated_at',
            'company',
            'employer',
            'location',
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        
        # --- Retrieve and validate company ---
        company_slug = validated_data.pop("company_slug", None)
        if not company_slug:
            raise serializers.ValidationError({"company_slug": "This field is required."})
        try:
            company = Company.objects.get(slug=company_slug)
        except Company.DoesNotExist:
            raise serializers.ValidationError({"company_slug": "Company with the given slug does not exist."})
        
        # --- Retrieve and validate location (city) ---
        location_slug = validated_data.pop("location_slug", None)
        if not location_slug:
            raise serializers.ValidationError({"location_slug": "This field is required."})
        try:
            city = City.objects.get(slug=location_slug)
        except City.DoesNotExist:
            raise serializers.ValidationError({"location_slug": "City with the given slug does not exist."})
        
        # --- Validate city matches the company's location ---
        if company.location != city:
            raise serializers.ValidationError({
                "location_slug": "The provided city does not match the company's location."
            })
        
        # --- Set foreign key fields ---
        validated_data["company"] = company
        validated_data["location"] = city
        validated_data["employer"] = request.user
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Forbid any updates to fields that set the foreign keys via slugs
        forbidden_fields = ["company", "employer", "location", "company_slug", "location_slug"]
        for field in forbidden_fields:
            if field in validated_data:
                raise serializers.ValidationError({field: f"You cannot change the {field} field."})
        return super().update(instance, validated_data)




class JobseekerResumeAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobseekerResumeAdvertisement
        fields = [
            "id",
            "job_seeker_profile",
            "resume",
            "title",
            "industry",
            "location",
            "slug",
            "description",
            "status",
            "gender",
            "soldier_status",
            "degree",
            "experience",
            "salary",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",         # Status is read-only via the API.
            "job_seeker_profile",
            "resume",
            "industry",
            "location",
            "gender",
            "soldier_status",
            "degree",
            "experience",
            "salary",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        """
        Create a JobseekerResumeAdvertisement instance by using the resume instance
        (provided via serializer context) to fill in several fields automatically.
        
        This method:
          - Expects the view to supply a 'resume' in the serializer context.
          - Uses the resume to set:
              • job_seeker_profile
              • gender
              • soldier_status
              • degree
              • experience
              • salary (from expected_salary)
              • industry
              • location
          - Generates a slug if one is not provided.
        """
        resume = self.context.get("resume")
        if not resume:
            raise serializers.ValidationError({"resume": "JobSeeker resume must be provided in context."})
            
        # Auto-populate fields from the resume instance.
        validated_data["job_seeker_profile"] = resume.job_seeker_profile
        validated_data["gender"] = resume.gender
        validated_data["soldier_status"] = resume.soldier_status
        validated_data["degree"] = resume.degree
        validated_data["experience"] = resume.experience
        validated_data["salary"] = resume.expected_salary
        validated_data["industry"] = resume.industry
        validated_data["location"] = resume.location
        validated_data["resume"] = resume

        # Auto-generate a slug, e.g., using the title or by falling back to resume data.
        if not validated_data.get("slug"):
            title = validated_data.get("title")
            if title:
                validated_data["slug"] = slugify(title)
            else:
                validated_data["slug"] = slugify(f"resume-ad-{resume.pk}")
                
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Forbid updates to fields that need to remain consistent with the resume.
        Only allow updating fields such as 'title' and 'description', while forbidding
        changes to any key fields auto-populated from the resume.
        """
        forbidden_fields = [
            "job_seeker_profile",
            "resume",
            "industry",
            "location",
            "gender",
            "soldier_status",
            "degree",
            "experience",
            "salary",
            "slug",
        ]
        for field in forbidden_fields:
            if field in validated_data:
                raise serializers.ValidationError({field: "You cannot change this field."})
        return super().update(instance, validated_data)

class ApplicationSerializer(serializers.ModelSerializer):
    # Nested serializers for related fields
    job_seeker = JobSeekerProfileSerializer(read_only=True)  # Display job seeker profile details
    resume = JobSeekerResumeSerializer(read_only=True)  # Display resume details
    advertisement = JobAdvertisementSerializer(read_only=True)  # Display advertisement details

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

