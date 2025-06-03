from django.shortcuts import get_object_or_404  
# وارد کردن تابع get_object_or_404 برای واکشی یک شیء از دیتابیس یا پرتاب خطای 404 اگر شیء پیدا نشود

from rest_framework import viewsets, status, permissions  
# ایمپورت ماژول‌های viewsets برای مدیریت ویوست‌ها، status برای کدهای وضعیت HTTP و permissions برای مدیریت سطح دسترسی

from rest_framework.views import Response  
# ایمپورت کلاس Response برای ارسال پاسخ‌های HTTP

from .models import SubscriptionOrder  
# ایمپورت مدل SubscriptionOrder از فایل models جهت استفاده در ویو

from .serializers import SubscriptionOrderSerializer  
# ایمپورت سریالایزر SubscriptionOrderSerializer برای مدیریت داده‌های ورودی و خروجی

from Advertisements.models import Advertisement  
# ایمپورت مدل Advertisement برای مدیریت آگهی‌های مرتبط با سفارش

from Subscriptions.models import SubscriptionPlan, AdvertisementSubscription  
# ایمپورت مدل‌های SubscriptionPlan و AdvertisementSubscription برای مدیریت طرح‌ها و اشتراک‌های مرتبط




# =============================================================================
# ویو SubscriptionOrderViewSet برای مدیریت سفارشات اشتراک
# =============================================================================
class SubscriptionOrderViewSet(viewsets.ViewSet):
    """
    ویوست برای مدیریت عملیات سفارشات اشتراک شامل عملیات لیست، دریافت جزئیات و ایجاد سفارش.
    """

    permission_classes = [permissions.IsAuthenticated]  
    # تنها کاربران احراز هویت‌شده می‌توانند به این ویوست دسترسی داشته باشند

    def list(self, request):
        """
        دریافت لیستی از تمامی سفارشات (یا سفارشات کاربر جاری).
        """
        queryset = SubscriptionOrder.objects.all()  # واکشی تمامی سفارشات از دیتابیس
        if request.user.is_staff:  
            # اگر کاربر admin باشد، تمامی سفارشات نمایش داده می‌شود
            serializer = SubscriptionOrderSerializer(queryset, many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)  
        else:
            # اگر کاربر معمولی باشد، تنها سفارشات متعلق به خودش نمایش داده می‌شود
            user_order = queryset.filter(owner=request.user)  
            serializer = SubscriptionOrderSerializer(user_order, many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)  

    def retrieve(self, request, order_id):
        """
        دریافت جزئیات یک سفارش خاص بر اساس order_id.
        """
        instance = get_object_or_404(SubscriptionOrder, id=order_id)  
        # واکشی سفارش از دیتابیس بر اساس order_id یا ارسال خطای 404 اگر یافت نشود
        if request.user == instance.owner or request.user.is_staff:  
            # بررسی اینکه آیا کاربر مالک سفارش یا admin است
            serializer = SubscriptionOrderSerializer(instance)  
            return Response(serializer.data, status=status.HTTP_200_OK)  
        else:
            # در صورت نداشتن مجوز دسترسی، ارسال پاسخ خطای دسترسی
            return Response({"Massage": "شما برای دسترسی به این اطلاعات مجوز ندارید."})

    def create(self, request):
        """
        ایجاد یک سفارش جدید.
        """

        # ایجاد سریالایزر با داده‌های ورودی و ارسال مقادیر context شامل اطلاعات طرح، آگهی و اشتراک
        serializer = SubscriptionOrderSerializer(data=request.data)
        if serializer.is_valid():
            # اگر داده‌ها معتبر باشند، یک سفارش جدید ایجاد و ذخیره می‌شود
            serializer.save()
            return Response({"Massage": "سفارش با موفقیت ساخته شد"}, status=status.HTTP_200_OK)  
        else:
            # در صورت بروز خطا در داده‌های ورودی، پاسخ خطای 400 ارسال می‌شود
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)