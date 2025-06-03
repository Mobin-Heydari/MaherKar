from rest_framework import viewsets, permissions, status

from rest_framework.response import Response

from rest_framework.generics import get_object_or_404 

from Profiles.models import JobSeekerProfile

from .models import JobAdvertisement, ResumeAdvertisement, Application

from .serializers import Advertisement, JobAdvertisementSerializer, ResumeAdvertisementSerializer, ApplicationSerializer


class JobAdvertisementViewSet(viewsets.ViewSet):
    
    def list(self, request):
        # دریافت تمامی نمونه‌های JobAdvertisement (آگهی‌های کارفرما)
        queryset = JobAdvertisement.objects.all()
        # سریالایز کردن لیست آگهی‌های کارفرما
        serializer = JobAdvertisementSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        query = get_object_or_404(JobAdvertisement, id=pk)
        serializer = JobAdvertisementSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        # بررسی می‌شود که کاربر دارای نوع کاربری (user_type) "EM" (کارفرما) است.
        if request.user.user_type == "EM":
            serializer = JobAdvertisementSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()  # ایجاد یک آگهی کارفرما جدید
                return Response({"Massage": "Job created."}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # اگر کاربر کارفرما نباشد، ارسال پیام خطا
            return Response({"Massage": "You are not a employer."}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk):
        # واکشی آگهی کارفرما بر اساس شناسه (pk)
        query = get_object_or_404(JobAdvertisement, id=pk)
        # چک می‌شود که آیا درخواست‌دهنده مالک آگهی (advertisement.owner) است یا یک admin (is_staff)
        if query.advertisement.owner == request.user or request.user.is_staff:
            # ایجاد سریالایزر جهت به‌روزرسانی جزئی (partial update)
            serializer = JobAdvertisementSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()  # ذخیره تغییرات
                return Response(
                    {
                        "Massage": "Job ad updated.",
                        "data": serializer.data
                    }, status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Massage": "You dont have the permissions."}, status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, pk):
        # واکشی آگهی کارفرما مرتبط که شناسه آن pk و فیلد advertisement برابر با main_ad باشد
        query = get_object_or_404(JobAdvertisement, id=pk)
        if query.advertisement.owner == request.user or request.user.is_staff:
            query.delete()    # حذف آگهی کارفرما
            return Response({"Massage": "The advertisement deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Massage": "You dont have the permissions."}, status=status.HTTP_403_FORBIDDEN)
        


class ResumeAdvertisementViewSet(viewsets.ViewSet):
    
    def list(self, request):
        # دریافت تمامی آگهی‌های رزومه کارجو
        queryset = ResumeAdvertisement.objects.all()
        serializer = ResumeAdvertisementSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        # واکشی آگهی رزومه کارجو بر اساس اسلاگ آگهی عمومی (id)
        query = get_object_or_404(ResumeAdvertisement, id=pk)
        serializer = ResumeAdvertisementSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        # بررسی می‌شود که کاربر دارای نوع کاربری "JS" (جوینده کار) است.
        if request.user.user_type == "JS":
            # ایجاد سریالایزر جهت ایجاد آگهی رزومه؛ context شامل شناسه پروفایل و request ارسال می‌شود
            serializer = ResumeAdvertisementSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()  # ایجاد ResumeAdvertisement جدید
                return Response({"Massage": "Resume created."}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Massage": "You are not job seeker for creating resume ad"}, status=status.HTTP_200_OK)

    def update(self, request, pk):
        # واکشی آگهی رزومه کارجو بر اساس شناسه (pk)
        query = get_object_or_404(ResumeAdvertisement, id=pk)
        # اگر مالک آگهی عمومی برابر با کاربر درخواست‌دهنده یا کاربر ادمین باشد
        if query.advertisement.owner == request.user or request.user.is_staff:
            # ایجاد سریالایزر جهت به‌روزرسانی جزئی
            serializer = ResumeAdvertisementSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()  # ذخیره تغییرات
                return Response(
                    {
                        "Massage": "Resume ad updated.",
                        "data": serializer.data
                    }, status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Massage": "You dont have the permissions."}, status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, pk):
        # واکشی آگهی رزومه کارجو مرتبط بر اساس شناسه (pk) و آگهی مربوطه (main_ad)
        query = get_object_or_404(ResumeAdvertisement, id=pk)
        if query.advertisement.owner == request.user or request.user.is_staff:
            query.delete()    # حذف آگهی رزومه کارجو
            return Response({"Massage": "The advertisement deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Massage": "You dont have the permissions."}, status=status.HTTP_403_FORBIDDEN)



class ApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Application model operations.
    """
    queryset = Application.objects.all()  # تعیین queryset شامل تمامی نمونه‌های Application
    serializer_class = ApplicationSerializer  # سریالایزر مربوط به مدل Application
    permission_classes = [permissions.IsAuthenticated]  
    # تنها کاربران احراز هویت‌شده مجاز به دسترسی به این ویوست هستند

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()  # دریافت queryset (همه درخواست‌ها)
        serializer = self.get_serializer(queryset, many=True)  # سریالایز کردن لیست درخواست‌ها
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        # واکشی درخواست خاص بر اساس کلید اصلی (pk)؛ در صورت عدم وجود خطای 404 برگردانده می‌شود
        queryset = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(queryset)  # سریالایز کردن درخواست دریافت‌شده
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # ایجاد سریالایزر با داده‌های ورودی و context شامل request
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)  # اعتبارسنجی داده‌ها؛ در صورت عدم اعتبار خطا برمی‌گرداند
        serializer.save()  # ذخیره و ایجاد درخواست جدید؛ متد create سریالایزر خودکار کار را انجام می‌دهد
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        # واکشی نمونه درخواست بر اساس pk
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        # ساختن سریالایزر جهت به‌روز رسانی داده‌ها به‌صورت partial (جزئی)
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)  # اعتبارسنجی داده‌های ورودی
        serializer.save()  # ذخیره تغییرات در نمونه درخواست
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        # تنها کاربر ادمین اجازه حذف درخواست‌ها را دارد
        if request.user.is_staff:
            instance = get_object_or_404(self.get_queryset(), pk=pk)  # واکشی درخواست موردنظر
            instance.delete()  # حذف درخواست از دیتابیس
            return Response({"detail": "Application deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Massage": "You dont have the permissions"}, status=status.HTTP_403_FORBIDDEN)
