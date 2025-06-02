from rest_framework import serializers
import uuid

# Import related models from various apps.
from Industry.models import Industry
from Locations.models import City
from Companies.models import Company
from Subscriptions.models import AdvertisementSubscription
from Resumes.models import JobSeekerResume
from .models import JobAdvertisement, ResumeAdvertisement, Application




class JobAdvertisementSerializer(serializers.ModelSerializer):
    # Accepting 'company_id' and 'industry_id' as input only.
    company_id = serializers.CharField(write_only=True, required=False)
    industry_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = JobAdvertisement
        fields = '__all__'
        # These fields are automatically set by the create() method,
        # so they cannot be modified via the serializer.
        read_only_fields = ['employer', 'location', 'company']

    def create(self, validated_data):
        # Retrieve the current request and logged-in user.
        request = self.context.get('request')
        user = request.user

        # Extract and remove the company_id from validated_data.
        company_id = validated_data.pop('company_id', None)
        if company_id:
            try:
                # Use the default manager ('objects') to get the Company instance.
                company = Company.objects.get(id=company_id)
            except Company.DoesNotExist:
                raise serializers.ValidationError({'company': 'The company does not exist.'})
        else:
            raise serializers.ValidationError({'company_id': 'This field is required.'})
        
        # Extract and remove the industry_id from validated_data.
        industry_id = validated_data.pop('industry_id', None)
        if industry_id:
            try:
                # Retrieve the Industry instance.
                industry = Industry.objects.get(id=industry_id)
            except Industry.DoesNotExist:
                raise serializers.ValidationError({'industry': 'The industry does not exist.'})
        else:
            raise serializers.ValidationError({'industry_id': 'This field is required.'})

        # Verify that the user is the employer of the company or a staff member.
        if company.employer != user and not user.is_staff:
            raise serializers.ValidationError({'error': 'You are not the employer of this company.'})
        
        # Generate a unique identifier for the advertisement.
        generated_id = uuid.uuid4()
        
        # Create a new subscription for this advertisement.
        subscription = AdvertisementSubscription.objects.create()
        
        # Create the JobAdvertisement with all relationships and remaining data.
        advertisement = JobAdvertisement.objects.create(
            id=generated_id,
            subscription=subscription,
            industry=industry,
            company=company,
            location=company.location,  # Location is inferred from the company.
            employer=user,
            **validated_data  # Include other validated fields (e.g., title, description).
        )
        return advertisement

    def update(self, instance, validated_data):
        # Retrieve current request and user.
        request = self.context.get('request')
        user = request.user

        # Update simple fields.
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.gender = validated_data.get('gender', instance.gender)
        
        # Correct field naming for soldier_status.
        instance.soldier_status = validated_data.get('soldier_status', instance.soldier_status)
        instance.degree = validated_data.get('degree', instance.degree)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.job_type = validated_data.get('job_type', instance.job_type)

        # Optionally update the Industry if a new industry_id is provided.
        industry_id = validated_data.get('industry_id', None)
        if industry_id:
            try:
                industry = Industry.objects.get(id=industry_id)
                instance.industry = industry
            except Industry.DoesNotExist:
                raise serializers.ValidationError({'industry': 'The industry does not exist.'})
        
        # Optionally update the Location based on city_id if provided.
        city_id = validated_data.get('city_id', None)
        if city_id:
            try:
                location = City.objects.get(id=city_id)
                instance.location = location
            except City.DoesNotExist:
                raise serializers.ValidationError({'location': 'The location does not exist.'})
        
        # Allow staff users to update the advertisement's status.
        if user.is_staff:
            instance.status = validated_data.get('status', instance.status)
        
        # Persist the changes.
        instance.save()
        return instance


class ResumeAdvertisementSerializer(serializers.ModelSerializer):
    # Accepting input for a related city and industry.
    city_id = serializers.CharField(write_only=True, required=False)
    industry_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = ResumeAdvertisement
        fields = '__all__'
        # job_seeker, location, and resume are controlled by the system.
        read_only_fields = ['job_seeker', 'location', 'resume']

    def create(self, validated_data):
        # Get the request context to access the user.
        request = self.context.get('request')
        user = request.user
        
        # Extract and validate industry_id.
        industry_id = validated_data.pop('industry_id', None)
        if industry_id:
            try:
                industry = Industry.objects.get(id=industry_id)
            except Industry.DoesNotExist:
                raise serializers.ValidationError({'industry': 'The industry does not exist.'})
        else:
            raise serializers.ValidationError({'industry_id': 'This field is required.'})
        
        # Extract and validate city_id.
        city_id = validated_data.pop('city_id', None)
        if city_id:
            try:
                location = City.objects.get(id=city_id)
            except City.DoesNotExist:
                raise serializers.ValidationError({'location': 'The location does not exist.'})
        else:
            raise serializers.ValidationError({'city_id': 'This field is required.'})
        
        # Generate a new unique identifier.
        generated_id = uuid.uuid4()

        # Retrieve the JobSeekerResume for the logged in user.
        try:
            resume = JobSeekerResume.objects.get(job_seeker=user)
        except JobSeekerResume.DoesNotExist:
            raise serializers.ValidationError({'resume': 'No resume found for the job seeker.'})
        
        # Create a subscription for this resume advertisement.
        subscription = AdvertisementSubscription.objects.create()

        # Create the ResumeAdvertisement instance using the remaining validated data.
        advertisement = ResumeAdvertisement.objects.create(
            id=generated_id,
            subscription=subscription,
            industry=industry,
            location=location,
            job_seeker=user,
            resume=resume,
            **validated_data
        )
        return advertisement

    def update(self, instance, validated_data):
        # Get request and user from the serializer context.
        request = self.context.get('request')
        user = request.user

        # Update display fields.
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.gender = validated_data.get('gender', instance.gender)
        
        # Correct field naming: soldier_status (not solider_status).
        instance.soldier_status = validated_data.get('soldier_status', instance.soldier_status)
        instance.degree = validated_data.get('degree', instance.degree)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.job_type = validated_data.get('job_type', instance.job_type)

        # Update industry if new industry_id provided.
        industry_id = validated_data.get('industry_id', None)
        if industry_id:
            try:
                industry = Industry.objects.get(id=industry_id)
                instance.industry = industry
            except Industry.DoesNotExist:
                raise serializers.ValidationError({'industry': 'The industry does not exist.'})
        
        # Update location if a new city_id is provided.
        city_id = validated_data.get('city_id', None)
        if city_id:
            try:
                location = City.objects.get(id=city_id)
                instance.location = location
            except City.DoesNotExist:
                raise serializers.ValidationError({'location': 'The location does not exist.'})
        
        # Permit staff users to modify the advertisement's status.
        if user.is_staff:
            instance.status = validated_data.get('status', instance.status)

        instance.save()
        return instance


class ApplicationSerializer(serializers.ModelSerializer):
    # Accept advertisement_id as write-only input.
    advertisement_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Application
        fields = '__all__'
        # These fields are automatically set during creation, not updated via input.
        read_only_fields = ['job_seeker', 'advertisement', 'resume']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        
        # Extract and validate advertisement_id.
        advertisement_id = validated_data.pop('advertisement_id', None)
        if advertisement_id:
            try:
                advertisement = JobAdvertisement.objects.get(id=advertisement_id)
            except JobAdvertisement.DoesNotExist:
                raise serializers.ValidationError({'advertisement': 'The advertisement does not exist.'})
        else:
            raise serializers.ValidationError({'advertisement_id': 'This field is required.'})
        
        generated_id = uuid.uuid4()
        
        # Retrieve the job seeker's resume.
        try:
            resume = JobSeekerResume.objects.get(job_seeker=user)
        except JobSeekerResume.DoesNotExist:
            raise serializers.ValidationError({'resume': 'No resume found for the job seeker.'})
        
        # Create the Application instance. Use get() with a default value on cover_letter to avoid KeyError.
        application_instance = Application.objects.create(
            id=generated_id,
            advertisement=advertisement,
            job_seeker=user,
            resume=resume,
            cover_letter=validated_data.get('cover_letter', '')
        )
        return application_instance

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user

        # Update logic based on the role of the logged-in user.
        # Staff or the advertisement's employer may update status, notes, and cover letter.
        if user.is_staff or user == instance.advertisement.employer:
            instance.status = validated_data.get('status', instance.status)
            instance.employer_notes = validated_data.get('employer_notes', instance.employer_notes)
            instance.viewed_by_employer = validated_data.get('viewed_by_employer', instance.viewed_by_employer)
            instance.cover_letter = validated_data.get('cover_letter', instance.cover_letter)
        # The job seeker can update only the cover letter.
        elif user == instance.job_seeker:
            instance.cover_letter = validated_data.get('cover_letter', instance.cover_letter)

        instance.save()
        return instance
