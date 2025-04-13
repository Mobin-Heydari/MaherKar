from rest_framework import viewsets, status  
# ایمپورت ماژول viewsets برای مدیریت ویوست‌ها و status برای کدهای وضعیت HTTP

from rest_framework.response import Response  
# ایمپورت کلاس Response برای ارسال پاسخ‌های HTTP

from rest_framework.permissions import IsAuthenticated  
# ایمپورت کلاس IsAuthenticated برای محدود کردن دسترسی به کاربران احراز هویت‌شده

from django.shortcuts import get_object_or_404  
# ایمپورت تابع get_object_or_404 برای واکشی شیء از دیتابیس یا بازگرداندن خطای 404 در صورت عدم وجود

from .models import (
    JobSeekerReport,
    EmployerReport,
    AdvertisementReport
)  
# ایمپورت مدل‌های مرتبط با اپ گزارش‌ها

from .serializers import (
    JobSeekerReportSerializer,
    EmployerReportSerializer,
    AdvertisementReportSerializer
)  
# ایمپورت سریالایزرهای مرتبط با اپ گزارش‌ها



# =============================================================================
# ویو JobSeekerReportViewSet (مدیریت گزارش‌های جویندگان کار)
# =============================================================================
class JobSeekerReportViewSet(viewsets.ModelViewSet):
    """
    ویوست برای مدیریت گزارش‌های جویندگان کار.
    """
    queryset = JobSeekerReport.objects.all()  # تعیین مجموعه داده‌ها (queryset) برای واکشی گزارش‌ها از دیتابیس
    serializer_class = JobSeekerReportSerializer  # اتصال سریالایزر JobSeekerReport به ویوست
    permission_classes = [IsAuthenticated]  # محدود کردن دسترسی به کاربران احراز هویت‌شده
    lookup_field = 'id'  # استفاده از فیلد 'id' برای جستجو و بازیابی گزارش‌ها

    def list(self, request, *args, **kwargs):
        """
        لیست تمامی گزارش‌ها؛ فقط قابل دسترسی توسط مدیران (admin).
        """
        if request.user.is_staff:  # بررسی اینکه آیا کاربر admin است
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)  # سریالایز کردن داده‌ها به صورت لیست
            return Response(serializer.data)  # ارسال داده‌ها در پاسخ HTTP
        return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, id=None, *args, **kwargs):
        """
        دریافت جزئیات یک گزارش؛ قابل دسترسی توسط مدیران، گزارش‌دهنده، یا جوینده کار گزارش‌شده.
        """
        report = get_object_or_404(self.get_queryset(), id=id)  # واکشی گزارش بر اساس شناسه
        if request.user.is_staff or request.user == report.reporter or request.user == report.reported_jobseeker.user:
            serializer = self.get_serializer(report)  # سریالایز کردن داده‌های گزارش
            return Response(serializer.data)
        return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        """
        ایجاد یک گزارش جدید.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():  # بررسی معتبر بودن داده‌ها
            serializer.save(reporter=request.user)  # ثبت کاربر درخواست‌دهنده به عنوان گزارش‌دهنده
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, id=None, *args, **kwargs):
        """
        بروزرسانی یک گزارش موجود؛ فقط توسط مدیران یا گزارش‌دهنده قابل انجام است.
        """
        report = get_object_or_404(self.get_queryset(), id=id)
        if request.user.is_staff or request.user == report.reporter:
            serializer = self.get_serializer(report, data=request.data, partial=True)  # بروزرسانی جزئی
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "شما اجازه به‌روزرسانی این گزارش را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, id=None, *args, **kwargs):
        """
        حذف یک گزارش؛ فقط توسط مدیران یا گزارش‌دهنده قابل انجام است.
        """
        report = get_object_or_404(self.get_queryset(), id=id)
        if request.user.is_staff or request.user == report.reporter:
            report.delete()
            return Response({"message": "گزارش حذف شد"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "شما اجازه حذف این گزارش را ندارید"}, status=status.HTTP_403_FORBIDDEN)


# =============================================================================
# ویو EmployerReportViewSet (مدیریت گزارش‌های کارفرماها)
# =============================================================================
class EmployerReportViewSet(viewsets.ModelViewSet):
    """
    ویوست برای مدیریت گزارش‌های کارفرماها.
    """
    queryset = EmployerReport.objects.all()
    serializer_class = EmployerReportSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        """
        لیست تمامی گزارش‌ها؛ فقط قابل دسترسی توسط مدیران (admin).
        """
        if request.user.is_staff:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, id=None, *args, **kwargs):
        """
        دریافت جزئیات یک گزارش؛ قابل دسترسی توسط مدیران، گزارش‌دهنده، یا کارفرمای گزارش‌شده.
        """
        report = get_object_or_404(self.get_queryset(), id=id)
        if request.user.is_staff or request.user == report.reporter or request.user == report.reported_employer.user:
            serializer = self.get_serializer(report)
            return Response(serializer.data)
        return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        """
        ایجاد یک گزارش جدید.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reporter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, id=None, *args, **kwargs):
        """
        بروزرسانی یک گزارش موجود؛ فقط توسط مدیران یا گزارش‌دهنده قابل انجام است.
        """
        report = get_object_or_404(self.get_queryset(), id=id)
        if request.user.is_staff or request.user == report.reporter:
            serializer = self.get_serializer(report, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "شما اجازه به‌روزرسانی این گزارش را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, id=None, *args, **kwargs):
        """
        حذف یک گزارش؛ فقط توسط مدیران یا گزارش‌دهنده قابل انجام است.
        """
        report = get_object_or_404(self.get_queryset(), id=id)
        if request.user.is_staff or request.user == report.reporter:
            report.delete()
            return Response({"message": "گزارش حذف شد"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "شما اجازه حذف این گزارش را ندارید"}, status=status.HTTP_403_FORBIDDEN)


# =============================================================================
# ویو AdvertisementReportViewSet (مدیریت گزارش‌های آگهی‌ها)
# =============================================================================
class AdvertisementReportViewSet(viewsets.ModelViewSet):
    """
    ویوست برای مدیریت گزارش‌های آگهی‌ها.
    """
    queryset = AdvertisementReport.objects.all()
    serializer_class = AdvertisementReportSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        """
        لیست تمامی گزارش‌ها؛ فقط قابل دسترسی توسط مدیران (admin).
        """
        if request.user.is_staff:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, id=None, *args, **kwargs):
        """
        دریافت جزئیات یک گزارش؛ قابل دسترسی توسط مدیران یا گزارش‌دهنده.
        """
        report = get_object_or_404(self.get_queryset(), id=id)
        if request.user.is_staff or request.user == report.reporter:
            serializer = self.get_serializer(report)
            return Response(serializer.data)
        return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        """
        ایجاد یک گزارش جدید.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reporter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, id=None, *args, **kwargs):
        """
        بروزرسانی یک گزارش موجود؛ فقط توسط مدیران یا گزارش‌دهنده قابل انجام است.
        """
        report = get_object_or_404(self.get_queryset(), id=id)  # واکشی گزارش بر اساس شناسه
        if request.user.is_staff or request.user == report.reporter:  # بررسی دسترسی مدیر یا گزارش‌دهنده
            serializer = self.get_serializer(report, data=request.data, partial=True)  # بروزرسانی جزئی (partial=True)
            if serializer.is_valid():  # بررسی اعتبار داده‌های ورودی
                serializer.save()  # ذخیره تغییرات
                return Response(serializer.data, status=status.HTTP_200_OK)  # بازگرداندن داده‌های به‌روز شده
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # ارسال خطای 400 در صورت بروز مشکل
        return Response({"error": "شما اجازه به‌روزرسانی این گزارش را ندارید"}, status=status.HTTP_403_FORBIDDEN)  # خطای دسترسی

    def destroy(self, request, id=None, *args, **kwargs):
        """
        حذف یک گزارش؛ فقط توسط مدیران یا گزارش‌دهنده قابل انجام است.
        """
        report = get_object_or_404(self.get_queryset(), id=id)  # واکشی گزارش بر اساس شناسه
        if request.user.is_staff or request.user == report.reporter:  # بررسی دسترسی مدیر یا گزارش‌دهنده
            report.delete()  # حذف گزارش از دیتابیس
            return Response({"message": "گزارش حذف شد"}, status=status.HTTP_204_NO_CONTENT)  # ارسال پیام موفقیت در حذف
        return Response({"error": "شما اجازه حذف این گزارش را ندارید"}, status=status.HTTP_403_FORBIDDEN)  # خطای دسترسی
