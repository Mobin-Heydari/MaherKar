from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import SubscriptionPlan, AdvertisementSubscription
from .serializers import SubscriptionPlanSerializer, AdvertisementSubscriptionSerializer




class SubscriptionPlanViewSet(ViewSet):
    """
    ویوست برای مدیریت طرح‌های اشتراک.
    این کلاس شامل عملیات‌های لیست کردن، دریافت، ایجاد، بروزرسانی و حذف طرح‌های اشتراک است.
    """

    def list(self, request):
        """
        دریافت لیستی از تمامی طرح‌های اشتراک.
        """
        queryset = SubscriptionPlan.objects.all()
        serializer = SubscriptionPlanSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """
        دریافت جزئیات یک طرح اشتراک بر اساس شناسه (pk).
        """
        subscription_plan = get_object_or_404(SubscriptionPlan, pk=pk)
        serializer = SubscriptionPlanSerializer(subscription_plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        ایجاد یک طرح اشتراک جدید؛ فقط برای مدیران (admin).
        """
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = SubscriptionPlanSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        subscription_plan = serializer.save()

        return Response(SubscriptionPlanSerializer(subscription_plan).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """
        بروزرسانی یک طرح اشتراک موجود؛ فقط برای مدیران (admin).
        """
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
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
        حذف یک طرح اشتراک؛ فقط برای مدیران (admin).
        """
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        subscription_plan = get_object_or_404(SubscriptionPlan, pk=pk)
        subscription_plan.delete()
        return Response(
            {"detail": "Subscription Plan deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class AdvertisementSubscriptionViewSet(ViewSet):
    """
    ویوست برای مدیریت اشتراک‌های آگهی‌ها.
    این کلاس شامل عملیات‌های لیست کردن و دریافت جزئیات اشتراک آگهی است.
    """

    def list(self, request):
        """
        دریافت لیستی از تمامی اشتراک‌های آگهی.
        """
        queryset = AdvertisementSubscription.objects.all()
        serializer = AdvertisementSubscriptionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        دریافت جزئیات یک اشتراک آگهی بر اساس شناسه (pk).
        """
        subscription = get_object_or_404(AdvertisementSubscription, pk=pk)
        serializer = AdvertisementSubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)
