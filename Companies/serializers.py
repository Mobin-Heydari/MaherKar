from rest_framework import serializers
import uuid

from .models import Company
from Locations.models import City
from Locations.serializers import CitySerializer
from Users.serializers import UserSerializer


class CompanySerializer(serializers.ModelSerializer):
    city_id = serializers.CharField(write_only=True, required=False)
    location = CitySerializer(read_only=True)
    employer = UserSerializer(read_only=True)

    class Meta:
        model = Company
        fields = [
            "id",
            "employer",
            "name",
            "description",
            "website",
            "email",
            "phone_number",
            "city_id",
            "logo",
            "banner",
            "intro_video",
            "address",
            "location",
            "postal_code",
            "founded_date",
            "industry",
            "number_of_employees",
            "linkedin",
            "twitter",
            "instagram",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["employer", "location", "created_at", "updated_at"]


    def create(self, validated_data):
        """
        Create a new Company instance.

        Process:
        1. Extract the 'city_id' from the validated data and attempt to retrieve the corresponding City object.
        2. If 'city_id' is missing or invalid, raise a ValidationError.
        3. Generate a unique identifier for the new Company instance.
        4. Create and return the new Company using the provided validated data.
        
        Parameters:
            validated_data (dict): The validated data from the request.
            
        Returns:
            Company: The newly created Company instance.
            
        Raises:
            serializers.ValidationError: If 'city_id' is missing or does not correspond to an existing City.
        """
        request = self.context.get("request")
        employer = request.user

        city_id = validated_data.pop("city_id", None)
        if city_id is not None:
            try:
                location = City.objects.get(id=city_id)
            except City.DoesNotExist:
                raise serializers.ValidationError({"city_id": "City with the specified ID does not exist."})
        else:
            raise serializers.ValidationError({"city_id": "The 'city_id' field is required for creating a company."})
        
        generated_id = uuid.uuid4()

        company = Company.objects.create(
            employer=employer,
            location=location,
            id=generated_id,
            **validated_data
        )

        return company


    def update(self, instance, validated_data):
        """
        Update an existing Company instance.

        Process:
        1. Check if a new 'city_id' is provided. If so, retrieve the corresponding City and update the instance's location.
        2. For each field in the validated data, update the instance while preserving the current value if not provided.
        3. Save and return the updated Company instance.
        
        Note:
            The 'employer' field is read-only and will not be modified.
        
        Parameters:
            instance (Company): The existing Company instance to update.
            validated_data (dict): The validated data containing the fields to update.
            
        Returns:
            Company: The updated Company instance.
            
        Raises:
            serializers.ValidationError: If the provided 'city_id' does not correspond to an existing City.
        """
        city_id = validated_data.pop("city_id", None)
        if city_id is not None:
            try:
                location = City.objects.get(id=city_id)
            except City.DoesNotExist:
                raise serializers.ValidationError({"city_id": "City with the specified ID does not exist."})
            instance.location = location

        instance.name = validated_data.get("name", instance.name)

        instance.description = validated_data.get("description", instance.description)

        instance.website = validated_data.get("website", instance.website)

        instance.email = validated_data.get("email", instance.email)

        instance.phone_number = validated_data.get("phone_number", instance.phone_number)

        instance.logo = validated_data.get("logo", instance.logo)

        instance.banner = validated_data.get("banner", instance.banner)

        instance.intro_video = validated_data.get("intro_video", instance.intro_video)

        instance.address = validated_data.get("address", instance.address)

        instance.location = validated_data.get("location", instance.location)

        instance.postal_code = validated_data.get("postal_code", instance.postal_code)

        instance.founded_date = validated_data.get("founded_date", instance.founded_date)

        instance.industry = validated_data.get("industry", instance.industry)

        instance.number_of_employees = validated_data.get("number_of_employees", instance.number_of_employees)

        instance.linkedin = validated_data.get("linkedin", instance.linkedin)

        instance.twitter = validated_data.get("twitter", instance.twitter)

        instance.instagram = validated_data.get("instagram", instance.instagram)


        instance.save()
        return instance