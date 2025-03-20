from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer




# ویوست برای مدل کاربر
class UserViewSet(viewsets.ModelViewSet):
    """
        ویوست برای مدیریت عملیات مدل کاربر
    """

    # تعریف queryset برای ویوست
    queryset = User.objects.all()
    # تعریف کلاس سریالایزر برای ویوست
    serializer_class = UserSerializer
    # تعریف کلاس‌های دسترسی برای ویوست
    permission_classes = [IsAuthenticated]
    # مشخص کردن فیلد برای متدهای بازیابی (retrieve)
    lookup_field = 'username'

    # تعریف متد لیست برای ویوست
    def list(self, request, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت لیست کاربران
        """
        try:
            # بررسی اینکه آیا کاربر دارای سطح دسترسی استاف است
            if request.user.is_staff:
                # دریافت queryset
                queryset = self.get_queryset()
                # سریالایز کردن queryset
                serializer = self.get_serializer(queryset, many=True)
                # بازگرداندن داده‌های سریالایز شده
                return Response(serializer.data)
            else:
                # بازگرداندن پاسخ 403 اگر کاربر دسترسی نداشته باشد
                return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # بازگرداندن پاسخ 500 در صورت وقوع یک استثنا
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # تعریف متد بازیابی (retrieve) برای ویوست
    def retrieve(self, request, username, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت اطلاعات یک کاربر
        """
        try:
            # بررسی اینکه آیا کاربر استاف است یا همان کاربری است که درخواست کرده است
            if request.user.is_staff or request.user.username == username:
                # دریافت نمونه کاربر
                queryset = get_object_or_404(User, username=username)
                # سریالایز کردن نمونه کاربر
                serializer = self.get_serializer(queryset)
                # بازگرداندن داده‌های سریالایز شده
                return Response(serializer.data)
            else:
                # بازگرداندن پاسخ 403 اگر کاربر دسترسی نداشته باشد
                return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            # بازگرداندن پاسخ 404 اگر کاربر وجود نداشته باشد
            return Response({"error": "کاربر پیدا نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # بازگرداندن پاسخ 500 در صورت وقوع یک استثنا
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
