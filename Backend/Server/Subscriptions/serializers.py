from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import SubscriptionPlan, Duration, JobAdvertisementSubscription, JobseekerResumeAdvertisementSubscription

from Advertisements.models import JobAdvertisement, JobseekerResumeAdvertisement
from Advertisements.serializers import JobAdvertisementSerializer, JobseekerResumeAdvertisementSerializer
from Users.models import User


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'description', 'price_per_day', 'active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        return SubscriptionPlan.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price_per_day = validated_data.get('price_per_day', instance.price_per_day)
        instance.active = validated_data.get('active', instance.active)
        
        instance.save()
        return instance




class DurationSerializer(serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=SubscriptionPlan.objects.filter(active=True))

    class Meta:
        model = Duration
        fields = ['id', 'plan', 'day']
        read_only_fields = ['id']

    def create(self, validated_data):
        # Retrieve plan_name from the serializer context
        plan_name = self.context.get('plan_name')
        if not plan_name:
            raise serializers.ValidationError({"plan_name": "Plan name is required for creation."})
        
        # Look up the plan by its unique name
        try:
            plan = SubscriptionPlan.objects.get(name=plan_name)
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError({"plan_name": f"Plan with name '{plan_name}' does not exist."})
        
        # Add the plan to validated_data
        validated_data['plan'] = plan
        
        # Create and return the Duration instance
        return Duration.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Prevent changing the plan during updates
        if 'plan' in validated_data:
            raise serializers.ValidationError({"plan": "You cannot change the plan in the update method."})
        
        # Update other fields traditionally
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



class JobAdvertisementSubscriptionSerializer(serializers.ModelSerializer):
    advertisement = JobAdvertisementSerializer()
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
        read_only_fields = [
            'id', 'start_date', 'end_date', 'last_payment_date', 'next_payment_date',
            'created_at', 'updated_at', 'advertisement', 'user', 'plan', 'duration', 'payment_status'
        ]

    def create(self, validated_data):
        """
        Create a subscription using advertisement_slug and username from context.
        """
        # Retrieve advertisement_slug and username from the context
        advertisement_slug = self.context.get('advertisement_slug')
        username = self.context.get('username')

        if not advertisement_slug or not username:
            raise serializers.ValidationError({
                "detail": "Both 'advertisement_slug' and 'username' are required in the context."
            })

        # Get the advertisement instance
        advertisement = get_object_or_404(JobAdvertisement, slug=advertisement_slug)

        # Get the user instance
        user = get_object_or_404(User, username=username)

        # Add the advertisement and user to the validated data
        validated_data['advertisement'] = advertisement
        validated_data['user'] = user

        # Calculate the end date based on the duration
        duration_days = validated_data['duration'].day
        validated_data['end_date'] = validated_data['start_date'] + timezone.timedelta(days=duration_days)

        # Create the subscription instance
        return JobAdvertisementSubscription.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update only allowed fields. Prevent changes to immutable fields.
        """
        forbidden_fields = ['user', 'advertisement', 'plan', 'duration', 'payment_status']
        for field in forbidden_fields:
            if field in validated_data:
                raise serializers.ValidationError({field: f"{field} cannot be updated."})

        # Update the allowed fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save and return the updated instance
        instance.save()
        return instance



class JobseekerResumeAdvertisementSubscriptionSerializer(serializers.ModelSerializer):
    advertisement = JobseekerResumeAdvertisementSerializer()
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
        read_only_fields = [
            'id', 'start_date', 'end_date', 'last_payment_date', 'next_payment_date',
            'created_at', 'updated_at', 'advertisement', 'user', 'plan', 'duration', 'payment_status'
        ]

    def create(self, validated_data):
        """
        Create a subscription using advertisement_slug and username from context.
        """
        # Retrieve advertisement_slug and username from context
        advertisement_slug = self.context.get('advertisement_slug')
        username = self.context.get('username')

        if not advertisement_slug or not username:
            raise serializers.ValidationError({
                "detail": "Both 'advertisement_slug' and 'username' are required in the context."
            })

        # Get the advertisement instance
        advertisement = get_object_or_404(JobseekerResumeAdvertisement, slug=advertisement_slug)

        # Get the user instance
        user = get_object_or_404(User, username=username)

        # Add the advertisement and user to the validated data
        validated_data['advertisement'] = advertisement
        validated_data['user'] = user

        # Calculate the end date based on the duration
        duration_days = validated_data['duration'].day
        validated_data['end_date'] = validated_data['start_date'] + timezone.timedelta(days=duration_days)

        # Create the subscription instance
        return JobseekerResumeAdvertisementSubscription.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update only allowed fields. Prevent changes to immutable fields.
        """
        forbidden_fields = ['user', 'advertisement', 'plan', 'duration', 'payment_status']
        for field in forbidden_fields:
            if field in validated_data:
                raise serializers.ValidationError({field: f"{field} cannot be updated."})

        # Update the allowed fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save and return the updated instance
        instance.save()
        return instance
