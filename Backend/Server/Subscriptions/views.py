from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import (
    SubscriptionPlan,
    Duration,
    JobAdvertisementSubscription,
    JobseekerResumeAdvertisementSubscription
)
from .serializers import (
    SubscriptionPlanSerializer,
    DurationSerializer,
    JobAdvertisementSubscriptionSerializer,
    JobseekerResumeAdvertisementSubscriptionSerializer
)


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


class DurationViewSet(ViewSet):
    """
    ViewSet for managing Durations.
    """
    def list(self, request):
        queryset = Duration.objects.all()
        serializer = DurationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        duration = get_object_or_404(Duration, pk=pk)
        serializer = DurationSerializer(duration)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobAdvertisementSubscriptionViewSet(ViewSet):
    """
    ViewSet for managing Job Advertisement Subscriptions.
    """
    def list(self, request):
        queryset = JobAdvertisementSubscription.objects.all()
        serializer = JobAdvertisementSubscriptionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        subscription = get_object_or_404(JobAdvertisementSubscription, pk=pk)
        serializer = JobAdvertisementSubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobseekerResumeAdvertisementSubscriptionViewSet(ViewSet):
    """
    ViewSet for managing Jobseeker Resume Advertisement Subscriptions.
    """
    def list(self, request):
        queryset = JobseekerResumeAdvertisementSubscription.objects.all()
        serializer = JobseekerResumeAdvertisementSubscriptionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        subscription = get_object_or_404(JobseekerResumeAdvertisementSubscription, pk=pk)
        serializer = JobseekerResumeAdvertisementSubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)
