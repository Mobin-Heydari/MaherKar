from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.views import Response

from .models import SubscriptionOrder
from .serializers import SubscriptionOrderSerializer




class SubscriptionOrderViewSet(viewsets.ViewSet):
    """
    ویوست مدیریت سفارشات اشتراک.
    عملیات‌های لیست، جزئیات سفارش و ایجاد سفارش جدید در اینجا مدیریت می‌شود.
    """
    permission_classes = [permissions.IsAuthenticated]  # تنها کاربران احراز هویت شده به این ویو دسترسی دارند

    def list(self, request):
        """
        لیست تمامی سفارشات؛ اگر کاربر مدیر (admin) باشد، تمام سفارشات نمایش داده می‌شود،
        در غیر این صورت تنها سفارشات متعلق به کاربر جاری نمایش داده می‌شود.
        """
        queryset = SubscriptionOrder.objects.all()
        # بررسی سطح دسترسی کاربر جهت محدود کردن نتایج
        if request.user.is_staff:
            serializer = SubscriptionOrderSerializer(queryset, many=True)
        else:
            user_order = queryset.filter(owner=request.user)
            serializer = SubscriptionOrderSerializer(user_order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, order_id):
        """
        دریافت جزییات یک سفارش بر اساس شناسه 'order_id'.
        دسترسی فقط برای کاربری که سفارش را ساخته یا مدیر امکان‌پذیر است.
        """
        instance = get_object_or_404(SubscriptionOrder, id=order_id)
        # بررسی دسترسی: کاربر باید مالک سفارش یا مدیر باشد
        if request.user == instance.owner or request.user.is_staff:
            serializer = SubscriptionOrderSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"Massage": "شما برای دسترسی به این اطلاعات مجوز ندارید."})

    def create(self, request):
        """
        ایجاد یک سفارش جدید با استفاده از داده‌های ارسالی.
        اعتبارسنجی داده‌ها توسط SubscriptionOrderSerializer انجام می‌شود.
        """
        serializer = SubscriptionOrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"Massage": "سفارش با موفقیت ساخته شد"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
