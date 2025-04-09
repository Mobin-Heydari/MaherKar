from rest_framework.viewsets import ViewSet  
# وارد کردن کلاس ViewSet از DRF برای ساخت ویو کلاس‌بیس

from rest_framework.response import Response  
# وارد کردن کلاس Response جهت ارسال پاسخ‌های HTTP به کلاینت

from rest_framework import status  
# وارد کردن کدهای وضعیت HTTP (مانند 200، 201، 403 و غیره)

from django.shortcuts import get_object_or_404  
# تابع get_object_or_404 برای بازیابی شیء از دیتابیس یا پرتاب خطای 404 در صورت عدم وجود

from .models import SubscriptionPlan, AdvertisementSubscription  
# ایمپورت مدل‌های SubscriptionPlan و AdvertisementSubscription از فایل models

from .serializers import SubscriptionPlanSerializer, AdvertisementSubscriptionSerializer  
# ایمپورت سریالایزرهای مربوط به اشتراک‌ها از فایل serializers




# =============================================================================
# ویو SubscriptionPlanViewSet برای مدیریت طرح‌های اشتراک
# =============================================================================
class SubscriptionPlanViewSet(ViewSet):
    """
    ویوست برای مدیریت طرح‌های اشتراک.
    این کلاس شامل عملیات‌های لیست کردن، دریافت، ایجاد، بروزرسانی و حذف طرح‌های اشتراک است.
    """

    def list(self, request):
        """
        دریافت لیستی از تمامی طرح‌های اشتراک.
        """
        queryset = SubscriptionPlan.objects.all()  # واکشی همه رکوردهای SubscriptionPlan از دیتابیس
        serializer = SubscriptionPlanSerializer(queryset, many=True)  # سریالایز کردن لیست طرح‌ها
        return Response(serializer.data, status=status.HTTP_200_OK)  # ارسال پاسخ HTTP با داده‌های سریالایز شده

    def retrieve(self, request, pk=None):
        """
        دریافت جزئیات یک طرح اشتراک بر اساس شناسه (pk).
        """
        subscription_plan = get_object_or_404(SubscriptionPlan, pk=pk)  # واکشی رکورد SubscriptionPlan با شناسه pk
        serializer = SubscriptionPlanSerializer(subscription_plan)  # سریالایز کردن رکورد طرح
        return Response(serializer.data, status=status.HTTP_200_OK)  # ارسال پاسخ موفقیت‌آمیز با داده‌ها

    def create(self, request):
        """
        ایجاد یک طرح اشتراک جدید؛ فقط برای مدیران (admin).
        """
        if not request.user.is_staff:  # بررسی اینکه آیا کاربر مدیر است یا خیر
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        serializer = SubscriptionPlanSerializer(data=request.data)  # ایجاد سریالایزر با داده‌های ورودی درخواست
        serializer.is_valid(raise_exception=True)  # اعتبارسنجی داده‌ها؛ در صورت خطا، استثنا صادر می‌شود
        subscription_plan = serializer.save()  # ذخیره طرح اشتراک جدید در دیتابیس
        return Response(
            SubscriptionPlanSerializer(subscription_plan).data,  # داده‌های سریالایز شده برای طرح جدید
            status=status.HTTP_201_CREATED  # ارسال پاسخ موفقیت‌آمیز ایجاد
        )

    def update(self, request, pk=None):
        """
        بروزرسانی یک طرح اشتراک موجود؛ فقط برای مدیران (admin).
        """
        if not request.user.is_staff:  # بررسی اینکه آیا کاربر مدیر است یا خیر
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        subscription_plan = get_object_or_404(SubscriptionPlan, pk=pk)  # واکشی طرح اشتراک موجود بر اساس pk
        serializer = SubscriptionPlanSerializer(subscription_plan, data=request.data, partial=True)  
        # سریالایزر برای بروزرسانی جزئی (partial=True)
        serializer.is_valid(raise_exception=True)  # اعتبارسنجی داده‌ها
        updated_subscription_plan = serializer.save()  # ذخیره تغییرات در دیتابیس
        return Response(
            SubscriptionPlanSerializer(updated_subscription_plan).data,  # داده‌های سریالایز شده طرح بروزرسانی شده
            status=status.HTTP_200_OK  # ارسال پاسخ موفقیت‌آمیز بروزرسانی
        )

    def destroy(self, request, pk=None):
        """
        حذف یک طرح اشتراک؛ فقط برای مدیران (admin).
        """
        if not request.user.is_staff:  # بررسی اینکه آیا کاربر مدیر است یا خیر
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        subscription_plan = get_object_or_404(SubscriptionPlan, pk=pk)  # واکشی طرح اشتراک موجود بر اساس pk
        subscription_plan.delete()  # حذف طرح اشتراک از دیتابیس
        return Response({"detail": "Subscription Plan deleted successfully."}, status=status.HTTP_204_NO_CONTENT)  
        # ارسال پاسخ موفقیت‌آمیز حذف


# =============================================================================
# ویو AdvertisementSubscriptionViewSet برای مدیریت اشتراک‌های آگهی‌ها
# =============================================================================
class AdvertisementSubscriptionViewSet(ViewSet):
    """
    ویوست برای مدیریت اشتراک‌های آگهی‌ها.
    این کلاس شامل عملیات‌های لیست کردن و دریافت جزئیات اشتراک آگهی است.
    """

    def list(self, request):
        """
        دریافت لیستی از تمامی اشتراک‌های آگهی.
        """
        queryset = AdvertisementSubscription.objects.all()  # واکشی همه رکوردهای AdvertisementSubscription از دیتابیس
        serializer = AdvertisementSubscriptionSerializer(queryset, many=True)  # سریالایز کردن لیست اشتراک‌ها
        return Response(serializer.data, status=status.HTTP_200_OK)  # ارسال پاسخ HTTP با داده‌های سریالایز شده

    def retrieve(self, request, pk=None):
        """
        دریافت جزئیات یک اشتراک آگهی بر اساس شناسه (pk).
        """
        subscription = get_object_or_404(AdvertisementSubscription, pk=pk)  # واکشی رکورد AdvertisementSubscription با شناسه pk
        serializer = AdvertisementSubscriptionSerializer(subscription)  # سریالایز کردن رکورد اشتراک
        return Response(serializer.data, status=status.HTTP_200_OK)  # ارسال پاسخ موفقیت‌آمیز با داده‌های اشتراک
