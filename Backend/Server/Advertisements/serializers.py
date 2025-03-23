from rest_framework import serializers
from Advertisements.models import JobAdvertisement
from Companies.models import Company
from Companies.serializers import CompanySerializer
from Users.serializers import UserSerializer
from Industry.serializers import IndustrySerializer
from Locations.serializers import CitySerializer
from Locations.models import City  # used for lookup

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
