from django.shortcuts import get_object_or_404  # تابعی برای دریافت شیء یا ارسال خطای 404 در صورت عدم وجود
from rest_framework import viewsets  # استفاده از ویوست‌های مبتنی بر کلاس در Django REST Framework
from rest_framework.response import Response  # کلاس پاسخ جهت ارسال داده‌ها به کلاینت
from rest_framework import status  # وضعیت‌های HTTP جهت ارسال پاسخ‌های مناسب (مثلاً 403 یا 400)
from rest_framework.permissions import IsAuthenticated  # محدود کردن دسترسی به کاربران احراز هویت شده

# ایمپورت مدل‌های مربوط به پروفایل‌های جوینده کار، کارفرما، مدیر و پشتیبان
from .models import JobSeekerProfile, EmployerProfile, AdminProfile, SupportProfile
# ایمپورت سریالایزرهای مربوطه جهت تبدیل داده‌های مدل به JSON و بالعکس
from .serializers import (
    JobSeekerProfileSerializer,
    EmployerProfileSerializer,
    AdminProfileSerializer,
    SupportProfileSerializer
)



# --------------------------------------
# ویوست برای مدیریت پروفایل‌های جویندگان کار
# --------------------------------------
class JobSeekerProfileViewSet(viewsets.ViewSet):
    """
    ویوست برای مدیریت عملیات پروفایل‌های جویندگان کار.
    تنها کاربران احراز هویت شده مجاز به دسترسی هستند.
    """
    permission_classes = [IsAuthenticated]  # تنها کاربران احراز هویت شده دسترسی دارند
    lookup_field = 'pk'  # جستجو بر اساس نام کاربری در فیلد ارتباطی user

    def list(self, request, *args, **kwargs):
        """
        دریافت لیست تمامی پروفایل‌های جویندگان کار.
        تنها کاربران استاف (مدیر) قادر به مشاهده این لیست هستند.
        """
        if request.user.is_staff:
            queryset = JobSeekerProfile.objects.all()  # دریافت تمامی پروفایل‌های جوینده کار
            serializer = JobSeekerProfileSerializer(queryset, many=True)
            return Response(serializer.data)  # برگرداندن لیست پروفایل‌ها در صورت موفقیت
        else:
            # ارسال پیام خطای دسترسی در صورت عدم اجازه
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )

    def retrieve(self, request, pk, *args, **kwargs):
        """
        دریافت اطلاعات یک پروفایل جوینده کار بر اساس نام کاربری.
        تنها مدیر یا خود کاربر مجاز به مشاهده اطلاعات هستند.
        """
        if request.user.is_staff or request.user.username == pk:
            # در صورت دسترسی، پروفایل مورد نظر بازیابی می‌شود
            profile = get_object_or_404(JobSeekerProfile, user__id=pk)
            serializer = JobSeekerProfileSerializer(profile)
            return Response(serializer.data)
        else:
            # ارسال پیام خطای عدم دسترسی
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )
    
    def update(self, request, pk):
        """
        به‌روزرسانی اطلاعات یک پروفایل جوینده کار بر اساس نام کاربری.
        تنها مدیر یا خود کاربر مجاز به ویرایش اطلاعات هستند.
        """
        if request.user.is_staff or request.user.username == pk:
            # دریافت پروفایل به‌منظور به‌روزرسانی
            profile = get_object_or_404(JobSeekerProfile, user__id=pk)
            # سریالایزر با داده‌های ارسالی برای به‌روزرسانی نمونه مربوطه
            serializer = JobSeekerProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()  # ذخیره به‌روزرسانی در دیتابیس
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # ارسال پیام خطای اعتبارسنجی داده‌ها
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # ارسال پیام خطای عدم مجوز برای ویرایش
            return Response(
                {"error": "شما اجازه ویرایش این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )


# --------------------------------------
# ویوست برای مدیریت پروفایل‌های کارفرما
# --------------------------------------
class EmployerProfileViewSet(viewsets.ViewSet):
    """
    ویوست برای مدیریت عملیات پروفایل‌های کارفرما.
    تنها کاربران احراز هویت شده دسترسی دارند.
    """
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'  # استفاده از نام کاربری برای جستجو

    def list(self, request, *args, **kwargs):
        """
        دریافت لیست تمامی پروفایل‌های کارفرما.
        """
        if request.user.is_staff:
            queryset = EmployerProfile.objects.all()  # دریافت تمام پروفایل‌های کارفرما
            serializer = EmployerProfileSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )

    def retrieve(self, request, pk, *args, **kwargs):
        """
        دریافت اطلاعات یک پروفایل کارفرما بر اساس نام کاربری.
        تنها مدیر یا خود کاربر قادر به مشاهده اطلاعات هستند.
        """
        if request.user.is_staff or request.user.username == pk:
            profile = get_object_or_404(EmployerProfile, user__id=pk)
            serializer = EmployerProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )

    def update(self, request, pk):
        """
        به‌روزرسانی اطلاعات یک پروفایل کارفرما بر اساس نام کاربری.
        تنها مدیر یا خود کاربر مجاز به ویرایش هستند.
        """
        if request.user.is_staff or request.user.username == pk:
            profile = get_object_or_404(EmployerProfile, user__id=pk)
            serializer = EmployerProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "شما اجازه ویرایش این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )


# --------------------------------------
# ویوست برای مدیریت پروفایل‌های مدیر سیستم
# --------------------------------------
class AdminProfileViewSet(viewsets.ViewSet):
    """
    ویوست برای مدیریت عملیات پروفایل‌های مدیر.
    دسترسی فقط برای مدیران ارشد (superuser) مجاز است.
    """
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'  # جستجو بر اساس نام کاربری

    def list(self, request, *args, **kwargs):
        """
        دریافت لیست پروفایل‌های مدیر.
        دسترسی تنها برای مدیران ارشد.
        """
        if request.user.is_superuser:
            queryset = AdminProfile.objects.all()  # دریافت تمام پروفایل‌های مدیر
            serializer = AdminProfileSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )

    def retrieve(self, request, pk, *args, **kwargs):
        """
        دریافت اطلاعات یک پروفایل مدیر بر اساس نام کاربری.
        فقط مدیران ارشد قادر به مشاهده هستند.
        """
        if request.user.is_superuser:
            profile = get_object_or_404(AdminProfile, user__id=pk)
            serializer = AdminProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )

    def update(self, request, pk):
        """
        به‌روزرسانی اطلاعات یک پروفایل مدیر بر اساس نام کاربری.
        مدیر سیستم یا خود کاربر مجاز به ویرایش هستند.
        """
        if request.user.is_staff or request.user.username == pk:
            profile = get_object_or_404(AdminProfile, user__id=pk)
            serializer = AdminProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "شما اجازه ویرایش این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )


# --------------------------------------
# ویوست برای مدیریت پروفایل‌های پشتیبان
# --------------------------------------
class SupportProfileViewSet(viewsets.ViewSet):
    """
    ویوست برای مدیریت عملیات پروفایل‌های پشتیبان.
    دسترسی به این بخش فقط برای کاربران استاف یا خود صاحب پروفایل مجاز است.
    """
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'  # جستجو بر اساس نام کاربری

    def list(self, request, *args, **kwargs):
        """
        دریافت لیست تمامی پروفایل‌های پشتیبان.
        """
        if request.user.is_staff:
            queryset = SupportProfile.objects.all()  # دریافت تمام پروفایل‌های پشتیبان
            serializer = SupportProfileSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )
    
    def retrieve(self, request, pk, *args, **kwargs):
        """
        دریافت اطلاعات یک پروفایل پشتیبان بر اساس نام کاربری.
        """
        if request.user.is_staff:
            profile = get_object_or_404(SupportProfile, user__id=pk)
            serializer = SupportProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )
    
    def update(self, request, pk):
        """
        به‌روزرسانی اطلاعات یک پروفایل پشتیبان بر اساس نام کاربری.
        تنها کاربران استاف یا خود صاحب پروفایل مجاز به ویرایش هستند.
        """
        if request.user.is_staff or request.user.username == pk:
            profile = get_object_or_404(SupportProfile, user__id=pk)
            serializer = SupportProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "شما اجازه ویرایش این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )
