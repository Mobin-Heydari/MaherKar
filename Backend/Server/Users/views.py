from django.shortcuts import get_object_or_404  # وارد کردن تابع get_object_or_404 برای دریافت یک شیء از دیتابیس یا ارسال خطای 404 در صورت عدم وجود آن
from rest_framework import viewsets  # وارد کردن ویوست‌های Django REST Framework جهت ایجاد ویوهای مبتنی بر کلاس
from rest_framework.response import Response  # وارد کردن کلاس Response جهت ارسال پاسخ‌های HTTP به کلاینت
from rest_framework import status  # وارد کردن کدهای وضعیت HTTP برای استفاده در پاسخ‌ها
from rest_framework.permissions import IsAuthenticated  # وارد کردن کلاس دسترسی IsAuthenticated جهت محدود کردن دسترسی به کاربران وارد شده (authenticated)

from .models import User, IdCardInFormation  # وارد کردن مدل‌های User و IdCardInFormation از فایل models
from .serializers import UserSerializer, IdCardInFormationSerializer  # وارد کردن سریالایزرهای مرتبط برای تبدیل داده‌های مدل به فرمت JSON و بالعکس




# تعریف ViewSet جهت مدیریت عملیات مرتبط با اطلاعات کارت ملی
class IdCardViewSet(viewsets.ViewSet):

    # متد list برای دریافت لیست تمام اطلاعات کارت ملی
    def list(self, request):
        # بررسی سطح دسترسی؛ تنها در صورتی که کاربر دارای سطح دسترسی استاف (ادمین) باشد مجاز به دریافت لیست اطلاعات کارت ملی است
        if request.user.is_staff:
            # دریافت تمام نمونه‌های مدل IdCardInFormation از دیتابیس
            queryset = IdCardInFormation.objects.all()
            # سریالایز کردن queryset به فرمتی مناسب (لیستی از اشیاء)؛ many=True به معنی سریالایز کردن مجموعه‌ای از اشیاء است
            serializer = IdCardInFormationSerializer(queryset, many=True)
            # بازگرداندن پاسخ با داده‌های سریالایز شده و ارسال کد وضعیت 200 (موفقیت‌آمیز)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # در صورت عدم دسترسی کافی، پاسخ با کد وضعیت 403 (دسترسی غیرمجاز) ارسال می‌شود
            return Response({"Massage": "شما دسترسی به اطلاعات کارت ملی را ندارید"}, status=status.HTTP_403_FORBIDDEN)
    
    # متد retreive (اشاره به یک اشتباه املایی؛ بهتر است retrieve نامیده شود) برای دریافت یک نمونه خاص از اطلاعات کارت ملی بر اساس شناسه (pk)
    def retreive(self, request, pk):
        # تلاش برای دریافت شیء IdCardInFormation با شناسه ارائه شده؛ در صورت عدم وجود، خطای 404 برگردانده می‌شود
        query = get_object_or_404(IdCardInFormation, id=pk)
        # بررسی دسترسی: اگر کاربر سطح استاف داشته باشد یا شی مربوطه دارای اطلاعات کارت ملی (id_card_info) باشد
        if request.user.is_staff or query.id_card_info:
            # سریالایز کردن شی دریافت شده؛ (توجه: استفاده از UserSerializer ممکن است از نظر منطقی صحیح نباشد و بهتر از IdCardInFormationSerializer استفاده شود)
            serializer = UserSerializer(query)
            # ارسال داده‌های سریالایز شده به کلاینت
            return Response(serializer.data)
        else:
            # در صورت نداشتن دسترسی کافی، پاسخ خطای 403 ارسال می‌شود
            return Response({"Massage": "شما دسترسی برای دریافت اطلاعات را ندارید"}, status=status.HTTP_403_FORBIDDEN)
        
    # متد update برای به‌روزرسانی اطلاعات یک نمونه خاص از اطلاعات کارت ملی
    def update(self, request, pk):
        # دریافت شیء مورد نظر بر اساس شناسه؛ در صورت عدم وجود ارسال خطای 404
        query = get_object_or_404(IdCardInFormation, id=pk)
        # بررسی دسترسی: تنها کاربرانی که به عنوان استاف هستند یا شی دارای اطلاعات معتبر کارت ملی است، اجازه به‌روزرسانی دارند
        if request.user.is_staff or query.id_card_info:
            # سریالایز کردن شی دریافت شده؛ (دوباره توجه شود که استفاده از UserSerializer ممکن است منطقی نباشد، زیرا به‌روزرسانی باید با سریالایزر مرتبط با IdCardInFormation انجام شود)
            serializer = UserSerializer(query)
            # بررسی اعتبار داده‌های ورودی؛ سریالایزر بررسی می‌کند که آیا داده‌ها با قوانین تعریف شده مطابقت دارند یا نه
            if serializer.is_valid():
                # ذخیره تغییرات جدید در دیتابیس
                serializer.save()
                # ارسال داده‌های به‌روز شده به همراه کد وضعیت 200
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # در صورت بروز خطا در اعتبارسنجی، ارورها همراه با کد وضعیت 400 (درخواست نادرست) بازگردانده می‌شوند
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # در صورت نداشتن مجوز کافی برای به‌روزرسانی، پاسخ خطای 403 ارسال می‌شود
            return Response({"Massage": "شما دسترسی برای به‌روزرسانی اطلاعات را ندارید."}, status=status.HTTP_403_FORBIDDEN)




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
            queryset = get_object_or_404(User, id=pk)
            # سریالایز کردن نمونه کاربر دریافت‌شده به صورت مناسب جهت ارسال به کلاینت
            serializer = self.get_serializer(queryset)
            # ارسال داده‌های سریالایز شده به عنوان پاسخ
            return Response(serializer.data)
        else:
            # در صورت نداشتن مجوز کافی، پاسخ با کد وضعیت 403 ارسال می‌شود
            return Response({"Massage": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)
