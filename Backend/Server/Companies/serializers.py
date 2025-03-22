from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Company
from Users.models import User





class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = [
            'id',
            'employer',
            'name',
            'slug',
            'description',
            'website',
            'email',
            'phone_number',
            'logo',
            'banner',
            'intro_video',
            'address',
            'location',
            'postal_code',
            'founded_date',
            'industry',
            'number_of_employees',
            'linkedin',
            'twitter',
            'instagram',
            'created_at',
            'updated_at'
        ]
        # Set employer, slug, and timestamps as read-only fields
        read_only_fields = ['employer', 'slug', 'created_at', 'updated_at']
    


    def create(self, validated_data):
        # Fetch the employer_id from serializer context
        employer_id = self.context.get('employer_id')
        
        # Get the employer user object
        employer = get_object_or_404(User, id=employer_id)

        # Create the company instance
        company = Company.objects.create(
            employer=employer,
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            website=validated_data.get('website'),
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            logo=validated_data.get('logo'),
            banner=validated_data.get('banner'),
            intro_video=validated_data.get('intro_video'),
            address=validated_data.get('address'),
            location=validated_data.get('location'),
            postal_code=validated_data.get('postal_code'),
            founded_date=validated_data.get('founded_date'),
            industry=validated_data.get('industry'),
            number_of_employees=validated_data.get('number_of_employees'),
            linkedin=validated_data.get('linkedin'),
            twitter=validated_data.get('twitter'),
            instagram=validated_data.get('instagram')
        )

        return company

    
    def update(self, instance, validated_data):
        # Prevent updating the employer field by skipping validation for it
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.website = validated_data.get('website', instance.website)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.banner = validated_data.get('banner', instance.banner)
        instance.intro_video = validated_data.get('intro_video', instance.intro_video)
        instance.address = validated_data.get('address', instance.address)
        instance.location = validated_data.get('location', instance.location)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.founded_date = validated_data.get('founded_date', instance.founded_date)
        instance.industry = validated_data.get('industry', instance.industry)
        instance.number_of_employees = validated_data.get('number_of_employees', instance.number_of_employees)
        instance.linkedin = validated_data.get('linkedin', instance.linkedin)
        instance.twitter = validated_data.get('twitter', instance.twitter)
        instance.instagram = validated_data.get('instagram', instance.instagram)

        # Save and return the updated instance
        instance.save()
        return instance
