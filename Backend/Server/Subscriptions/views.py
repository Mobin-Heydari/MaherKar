from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import SubscriptionPlan, AdvertisementSubscription
from .serializers import SubscriptionPlanSerializer, AdvertisementSubscriptionSerializer



class SubscriptionPlanViewSet(ViewSet):
    """
    ViewSet for managing Subscription Plans.
    """
    def list(self, request):
        queryset = SubscriptionPlan.objects.all()
        serializer = SubscriptionPlanSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        subscription_plan = get_object_or_404(SubscriptionPlan, pk=pk)
        serializer = SubscriptionPlanSerializer(subscription_plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Create a new Subscription Plan (admin-only).
        """
        if not request.user.is_staff:  # Check if the user is an admin
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        serializer = SubscriptionPlanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscription_plan = serializer.save()
        return Response(
            SubscriptionPlanSerializer(subscription_plan).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, pk=None):
        """
        Update an existing Subscription Plan (admin-only).
        """
        if not request.user.is_staff:  # Check if the user is an admin
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        subscription_plan = get_object_or_404(SubscriptionPlan, pk=pk)
        serializer = SubscriptionPlanSerializer(subscription_plan, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_subscription_plan = serializer.save()
        return Response(
            SubscriptionPlanSerializer(updated_subscription_plan).data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):
        """
        Delete a Subscription Plan (admin-only).
        """
        if not request.user.is_staff:  # Check if the user is an admin
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        subscription_plan = get_object_or_404(SubscriptionPlan, pk=pk)
        subscription_plan.delete()
        return Response({"detail": "Subscription Plan deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class AdvertisementSubscriptionViewSet(ViewSet):
    """
    ViewSet for managing Job Advertisement Subscriptions.
    """

    def list(self, request):
        """
        Retrieve a list of all Job Advertisement Subscriptions.
        """
        queryset = AdvertisementSubscription.objects.all()
        serializer = AdvertisementSubscriptionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific Job Advertisement Subscription by its ID.
        """
        subscription = get_object_or_404(AdvertisementSubscription, pk=pk)
        serializer = AdvertisementSubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)
