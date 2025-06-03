from django.shortcuts import get_object_or_404  # وارد کردن تابع get_object_or_404 برای دریافت یک شیء از دیتابیس یا ارسال خطای 404 در صورت عدم وجود آن
from rest_framework import viewsets  # وارد کردن ویوست‌های Django REST Framework جهت ایجاد ویوهای مبتنی بر کلاس
from rest_framework.response import Response  # وارد کردن کلاس Response جهت ارسال پاسخ‌های HTTP به کلاینت
from rest_framework import status  # وارد کردن کدهای وضعیت HTTP برای استفاده در پاسخ‌ها
from rest_framework.permissions import IsAuthenticated  # وارد کردن کلاس دسترسی IsAuthenticated جهت محدود کردن دسترسی به کاربران وارد شده (authenticated)

from .models import User
from .serializers import UserSerializer






# تعریف ViewSet برای مدیریت عملیات مدل کاربر به صورت CRUD کامل
class UserViewSet(viewsets.ModelViewSet):
    """
        ویوست برای مدیریت عملیات مدل کاربر
    """

    queryset = User.objects.all()  # تعریف queryset شامل تمامی نمونه‌های مدل User از دیتابیس
    serializer_class = UserSerializer  # تعیین سریالایزر مرتبط با مدل User جهت تبدیل داده‌ها به JSON و بالعکس
    permission_classes = [IsAuthenticated]  # اعمال محدودیت: تنها کاربران احراز هویت شده می‌توانند به این ویو دسترسی داشته باشند
    lookup_field = 'pk'  # استفاده از فیلد pk به عنوان شناسه اصلی هنگام عملیات بازیابی (retrieve)

    # بازنویسی متد list برای مدیریت درخواست‌های GET جهت دریافت لیست کاربران
    def list(self, request, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت لیست کاربران
        """

        # بررسی می‌کند که آیا کاربر درخواست‌کننده دارای سطح دسترسی استاف است (ادمین)
        if request.user.is_staff:
            # دریافت queryset شامل تمامی نمونه‌های کاربران
            queryset = self.get_queryset()
            # سریالایز کردن queryset به صورت لیست؛ many=True به معنی تبدیل مجموعه‌ای از اشیاء است
            serializer = self.get_serializer(queryset, many=True)
            # بازگرداندن داده‌های سریالایز شده به عنوان پاسخ به کلاینت
            return Response(serializer.data)
        else:
            # سریالایز کردن user
            serializer = self.get_serializer(request.user)
            # بازگرداندن داده‌های سریالایز شده به عنوان پاسخ به کلاینت
            return Response(serializer.data)


    # تعریف متد retrieve جهت دریافت اطلاعات یک کاربر بر اساس نام کاربری
    def retrieve(self, request, pk, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت اطلاعات یک کاربر
        """

        # بررسی می‌کند که آیا کاربر دارای دسترسی استاف بوده و یا نام کاربری درخواست شده همان کاربری است که درخواست را ارسال کرده است
        if request.user.is_staff or request.user.id == pk:
            # تلاش برای دریافت نمونه کاربر با استفاده از نام کاربری؛ در صورت عدم یافتن، خطای 404 ارسال می‌شود
            instance = get_object_or_404(User, id=pk)
            # سریالایز کردن نمونه کاربر دریافت‌شده به صورت مناسب جهت ارسال به کلاینت
            serializer = self.get_serializer(instance)
            # ارسال داده‌های سریالایز شده به عنوان پاسخ
            return Response(serializer.data)
        else:
            # در صورت نداشتن مجوز کافی، پاسخ با کد وضعیت 403 ارسال می‌شود
            return Response({"Massage": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)
