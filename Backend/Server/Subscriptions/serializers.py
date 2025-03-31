from django.utils import timezone
from rest_framework import serializers
from .models import SubscriptionPlan, Duration, JobAdvertisementSubscription, JobseekerResumeAdvertisementSubscription



class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'description', 'price_per_day', 'active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']



class DurationSerializer(serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=SubscriptionPlan.objects.filter(active=True))

    class Meta:
        model = Duration
        fields = ['id', 'plan', 'day']
        read_only_fields = ['id']


class JobAdvertisementSubscriptionSerializer(serializers.ModelSerializer):
    advertisement = serializers.PrimaryKeyRelatedField(queryset=JobAdvertisementSubscription.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    plan = serializers.PrimaryKeyRelatedField(queryset=SubscriptionPlan.objects.filter(active=True))
    duration = serializers.PrimaryKeyRelatedField(queryset=Duration.objects.all())

    class Meta:
        model = JobAdvertisementSubscription
        fields = [
            'id', 'advertisement', 'user', 'plan', 'duration', 'payment_status',
            'start_date', 'end_date', 'last_payment_date', 'next_payment_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'start_date', 'end_date', 'created_at', 'updated_at']



class JobseekerResumeAdvertisementSubscriptionSerializer(serializers.ModelSerializer):
    advertisement = serializers.PrimaryKeyRelatedField(queryset=JobseekerResumeAdvertisementSubscription.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    plan = serializers.PrimaryKeyRelatedField(queryset=SubscriptionPlan.objects.filter(active=True))
    duration = serializers.PrimaryKeyRelatedField(queryset=Duration.objects.all())

    class Meta:
        model = JobseekerResumeAdvertisementSubscription
        fields = [
            'id', 'advertisement', 'user', 'plan', 'duration', 'payment_status',
            'start_date', 'end_date', 'last_payment_date', 'next_payment_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'start_date', 'end_date', 'created_at', 'updated_at']