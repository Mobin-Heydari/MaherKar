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

    def create(self, request):
        """
        Create a new Subscription Plan (admin-only).
        """
        if not request.user.is_staff:  # Check if the user is an admin
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

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
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

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
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        subscription_plan = get_object_or_404(SubscriptionPlan, pk=pk)
        subscription_plan.delete()
        return Response({"detail": "Subscription Plan deleted successfully."},
                        status=status.HTTP_204_NO_CONTENT)


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

    def create(self, request):
        """
        Create a new Duration (admin-only).
        """
        if not request.user.is_staff:  # Check if the user is an admin
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = DurationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        duration = serializer.save()
        return Response(
            DurationSerializer(duration).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, pk=None):
        """
        Update an existing Duration (admin-only).
        """
        if not request.user.is_staff:  # Check if the user is an admin
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        duration = get_object_or_404(Duration, pk=pk)
        serializer = DurationSerializer(duration, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_duration = serializer.save()
        return Response(
            DurationSerializer(updated_duration).data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):
        """
        Delete a Duration (admin-only).
        """
        if not request.user.is_staff:  # Check if the user is an admin
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        duration = get_object_or_404(Duration, pk=pk)
        duration.delete()
        return Response({"detail": "Duration deleted successfully."},
                        status=status.HTTP_204_NO_CONTENT)



class JobAdvertisementSubscriptionViewSet(ViewSet):
    """
    ViewSet for managing Job Advertisement Subscriptions.
    """

    def list(self, request):
        """
        Retrieve a list of all Job Advertisement Subscriptions.
        """
        queryset = JobAdvertisementSubscription.objects.all()
        serializer = JobAdvertisementSubscriptionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific Job Advertisement Subscription by its ID.
        """
        subscription = get_object_or_404(JobAdvertisementSubscription, pk=pk)
        serializer = JobAdvertisementSubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Create a Job Advertisement Subscription using context data.
        """
        advertisement_slug = request.data.get('advertisement_slug')
        username = request.user.username  # Assuming the user is authenticated

        serializer = JobAdvertisementSubscriptionSerializer(
            data=request.data,
            context={'advertisement_slug': advertisement_slug, 'username': username}
        )
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save()
        return Response(
            JobAdvertisementSubscriptionSerializer(subscription).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, pk=None):
        """
        Update an existing Job Advertisement Subscription instance.
        Only allows updates to allowed fields.
        """
        subscription = get_object_or_404(JobAdvertisementSubscription, pk=pk)

        serializer = JobAdvertisementSubscriptionSerializer(
            subscription, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        updated_subscription = serializer.save()
        return Response(
            JobAdvertisementSubscriptionSerializer(updated_subscription).data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):
        """
        Delete a Job Advertisement Subscription instance.
        """
        subscription = get_object_or_404(JobAdvertisementSubscription, pk=pk)
        subscription.delete()
        return Response(
            {"detail": "Subscription deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )



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

    def create(self, request):
        """
        Create a JobseekerResumeAdvertisementSubscription instance using context data.
        """
        advertisement_slug = request.data.get('advertisement_slug')
        username = request.user.username  # Assuming the user is authenticated

        serializer = JobseekerResumeAdvertisementSubscriptionSerializer(
            data=request.data,
            context={'advertisement_slug': advertisement_slug, 'username': username}
        )
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save()
        return Response(
            JobseekerResumeAdvertisementSubscriptionSerializer(subscription).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, pk=None):
        """
        Update an existing JobseekerResumeAdvertisementSubscription instance.
        Only allows updates to fields that are not forbidden.
        """
        subscription = get_object_or_404(JobseekerResumeAdvertisementSubscription, pk=pk)

        serializer = JobseekerResumeAdvertisementSubscriptionSerializer(
            subscription, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        updated_subscription = serializer.save()
        return Response(
            JobseekerResumeAdvertisementSubscriptionSerializer(updated_subscription).data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):
        """
        Delete a JobseekerResumeAdvertisementSubscription instance.
        """
        subscription = get_object_or_404(JobseekerResumeAdvertisementSubscription, pk=pk)
        subscription.delete()
        return Response(
            {"detail": "Subscription deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

