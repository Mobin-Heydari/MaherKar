from rest_framework import serializers

from Advertisements.models import Advertisement, JobAdvertisement, ResumeAdvertisement

from Subscriptions.models import SubscriptionPlan, AdvertisementSubscription

from .models import SubscriptionOrder

import uuid 




class SubscriptionOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionOrder
        fields = "__all__"


    def create(self, validated_data):
        request = self.context.get('request')

        user = request.user

        plan_id = validated_data.pop('plan_id', None)
        if plan_id:
            try:
                plan = SubscriptionPlan.objects.get(id=plan_id)
            except SubscriptionPlan.DoesNotExist:
                raise serializers.ValidationError({'plan': 'The plan does not exist.'})
        else:
            raise serializers.ValidationError({'plan_id': 'This field is required.'})
        
        advertisement_id = validated_data.pop('advertisement_id', None)
        if advertisement_id:
            try:
                advertisement = Advertisement.objects.get(id=advertisement_id)
            except Advertisement.DoesNotExist:
                raise serializers.ValidationError({'advertisement': 'The advertisement does not exist.'})
        else:
            raise serializers.ValidationError({'advertisement_id': 'This field is required.'})
        
        
        if advertisement.ad_type == 'J':
            if advertisement.job_advertisement.employer == user or user.is_staff:
                ad_type = "J"
            else:
                raise serializers.ValidationError({'error': 'Uncommon security error for job advertisement.'})
            
        if advertisement.ad_type == 'R':
            if advertisement.resume_advertisement.job_seeker == user or user.is_staff:
                ad_type = "R"
            else:
                raise serializers.ValidationError({'error': 'Uncommon security error for resume advertisement.'})
        

        subscription = advertisement.subscription
        
        price_per_day = plan.price_per_day

        duration = validated_data.get('duration')
        duration_price = duration * price_per_day
        taks_price = duration_price * 10 // 100

        total_price = duration_price + taks_price

        order_id = uuid.uuid4()

        order = SubscriptionOrder.objects.create(
            plan=plan,
            owner=user,
            duration=duration,
            order_id=order_id,
            total_price=total_price,
            advertisement=advertisement,
            advertisement_subscription=subscription,
            ad_type=ad_type
        )

        order.save()
        return order