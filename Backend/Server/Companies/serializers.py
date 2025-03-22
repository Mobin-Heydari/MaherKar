from rest_framework import serializers
from .models import Company




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

        read_only_fields = ['slug', 'created_at', 'updated_at']
