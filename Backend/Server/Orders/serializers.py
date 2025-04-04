from rest_framework import serializers

from Advertisements.models import Advertisement
from Subscriptions.models import SubscriptionPlan, AdvertisementSubscription

from .models import SubscriptionOrder

import uuid





class SubscriptionOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionOrder
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get('request')
        plan_id = self.context.get('plan_id')
        ad_slug = self.context.get('ad_slug')
        subscription_id = self.context.get('subscription_id')
        
        plan = SubscriptionPlan.objects.get(id=plan_id)
        advertisement = Advertisement.objects.get(slug=ad_slug)
        subscription = AdvertisementSubscription.objects.get(id=subscription_id)

        price = plan.price_per_day

        duration = validated_data.get('durations')

        duration_price = duration * price
        taks_price = duration_price * 10 // 100

        total_price = duration_price + taks_price

        order_id = uuid.uuid4()

        order = SubscriptionOrder.objects.create(
            plan=plan,
            owner=request.user,
            advertisement=advertisement,
            advertisement_subscription=subscription,
            total_price=total_price,
            duration=duration,
            order_id=order_id,
        )

        order.save()
        return order
    