from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, permissions
from rest_framework.views import Response

from .models import SubscriptionOrder
from .serializers import SubscriptionOrderSerializer

from Advertisements.models import Advertisement
from Subscriptions.models import SubscriptionPlan, AdvertisementSubscription






class SubscriptionOrderViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = SubscriptionOrder.objects.all()
        if request.user.is_staff:
            serializer = SubscriptionOrderSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user_order = queryset.filter(owner=request.user)
            serializer = SubscriptionOrderSerializer(user_order, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, order_id):
        query = get_object_or_404(SubscriptionOrder, order_id=order_id)
        if request.user == query.owner or request.user.is_staff:
            serializer = SubscriptionOrderSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"Massage": "You dont have the permission to accsses this data."})
    
    def create(self, request, plan_id, subscription_id, ad_slug):

        plan = get_object_or_404(SubscriptionPlan, id=plan_id)

        subscription = get_object_or_404(AdvertisementSubscription, id=subscription_id)

        advertisement = get_object_or_404(
            Advertisement,
            slug=ad_slug,
            owner=request.user,
            subscription=subscription
        )

        serializer = SubscriptionOrderSerializer(
            data=request.data,
            context={
                'request': request,
                'plan_id': plan_id,
                'subscription_id': subscription_id,
                'ad_slug': ad_slug
            }
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"Massage": "Order created secsussfully."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)