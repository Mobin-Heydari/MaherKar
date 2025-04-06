from rest_framework import serializers
from .models import (
    ReportCategory,
    JobSeekerReport,
    EmployerReport,
    AdvertisementReport,
)


class ReportCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for ReportCategory.
    """
    class Meta:
        model = ReportCategory
        fields = ['id', 'name', 'description']


class JobSeekerReportSerializer(serializers.ModelSerializer):
    """
    Serializer for JobSeekerReport.
    """
    reported_jobseeker_username = serializers.ReadOnlyField(source='reported_jobseeker.user.username')
    reporter_username = serializers.ReadOnlyField(source='reporter.username')

    class Meta:
        model = JobSeekerReport
        fields = [
            'id',
            'status',
            'reported_jobseeker',
            'reported_jobseeker_username',
            'reporter',
            'reporter_username',
            'category',
            'description',
            'created_at',
        ]

    def create(self, validated_data):
        """
        Custom creation logic for JobSeekerReport.
        """
        return JobSeekerReport.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Custom update logic for JobSeekerReport.
        """
        instance.status = validated_data.get('status', instance.status)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class EmployerReportSerializer(serializers.ModelSerializer):
    """
    Serializer for EmployerReport.
    """
    reported_employer_username = serializers.ReadOnlyField(source='reported_employer.user.username')
    reporter_username = serializers.ReadOnlyField(source='reporter.username')

    class Meta:
        model = EmployerReport
        fields = [
            'id',
            'status',
            'reported_employer',
            'reported_employer_username',
            'reporter',
            'reporter_username',
            'category',
            'description',
            'created_at',
        ]

    def create(self, validated_data):
        """
        Custom creation logic for EmployerReport.
        """
        return EmployerReport.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Custom update logic for EmployerReport.
        """
        instance.status = validated_data.get('status', instance.status)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance



class AdvertisementReportSerializer(serializers.ModelSerializer):
    """
    Serializer for AdvertisementReport.
    """
    reporter_username = serializers.ReadOnlyField(source='reporter.username')

    class Meta:
        model = AdvertisementReport
        fields = [
            'id',
            'status',
            'job_advertisement',
            'reporter',
            'reporter_username',
            'category',
            'description',
            'created_at',
        ]

    def create(self, validated_data):
        """
        Custom creation logic for AdvertisementReport.
        """
        return AdvertisementReport.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Custom update logic for AdvertisementReport.
        """
        instance.status = validated_data.get('status', instance.status)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


