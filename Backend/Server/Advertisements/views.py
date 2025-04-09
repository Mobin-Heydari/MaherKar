from rest_framework import viewsets, permissions, status  
# وارد کردن کلاس‌های viewsets برای ساخت ویو کلاس‌بیس، permissions برای مدیریت دسترسی و status برای کدهای وضعیت HTTP

from rest_framework.response import Response  
# استفاده برای ارسال پاسخ‌های HTTP به‌صورت دقیق

from rest_framework.generics import get_object_or_404  
# استفاده از تابع get_object_or_404 جهت بازیابی شیء از دیتابیس یا پرتاب خطای 404 در صورت عدم وجود

from Profiles.models import JobSeekerProfile  
# ایمپورت مدل JobSeekerProfile از اپ Profiles جهت استفاده در ویوها

from .models import Advertisement, JobAdvertisement, ResumeAdvertisement, Application  
# ایمپورت مدل‌های مربوط به آگهی‌ها: Advertisement (آگهی عمومی)، JobAdvertisement (آگهی کارفرما)، 
# ResumeAdvertisement (آگهی رزومه کارجو) و Application (درخواست)

from .serializers import AdvertisementSerializer, JobAdvertisementSerializer, ResumeAdvertisementSerializer, ApplicationSerializer  
# ایمپورت سریالایزرهای مربوط به مدل‌های فوق جهت تبدیل داده‌ها به فرمت JSON و بالعکس




# ======================================================================
# AdvertisementViewSet: ویوست برای مدیریت آگهی‌های عمومی
# ======================================================================
class AdvertisementViewSet(viewsets.ViewSet):

    def list(self, request):
        # دریافت تمامی آگهی‌های عمومی از مدل Advertisement
        queryset = Advertisement.objects.all()
        # سریالایز کردن queryset به صورت لیست (many=True)
        serializer = AdvertisementSerializer(queryset, many=True)
        # بازگرداندن داده‌های سریالایز شده به همراه کد HTTP 200 (موفقیت‌آمیز)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, slug):
        # واکشی یک آگهی عمومی بر مبنای فیلد slug؛ در صورت عدم وجود خطای 404 داده می‌شود
        query = get_object_or_404(Advertisement, slug=slug)
        # سریالایز کردن آگهی دریافت شده
        serializer = AdvertisementSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, slug):
        # واکشی آگهی عمومی بر اساس slug
        query = get_object_or_404(Advertisement, slug=slug)
        # ایجاد سریالایزر جهت به‌روزرسانی شماره داده‌های ورودی به‌صورت partial (جزئی)
        serializer = AdvertisementSerializer(query, data=request.data, partial=True, context={'request': request})
        # بررسی مجوز: اگر کاربر درخواست‌دهنده همان مالک آگهی یا admin باشد
        if request.user == query.owner or request.user.is_staff:
            if serializer.is_valid():
                serializer.save()  # ذخیره تغییرات در آگهی
                return Response(
                    {
                        'Message': "Advertisemenet updated.",  # پیام موفقیت
                        "Data": serializer.data
                    }, 
                    status=status.HTTP_200_OK
                )
            else:
                # ارسال خطاهای اعتبارسنجی در صورت بروز مشکل
                return Response({"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # در صورت عدم مجوز، ارسال پاسخ خطای 403 (ممنوع)
            return Response({"Massage": "You dont have permission"}, status=status.HTTP_403_FORBIDDEN)
        

# ======================================================================
# JobAdvertisementViewSet: ویوست برای مدیریت آگهی‌های کارفرما
# ======================================================================
class JobAdvertisementViewSet(viewsets.ViewSet):
    
    def list(self, request):
        # دریافت تمامی نمونه‌های JobAdvertisement (آگهی‌های کارفرما)
        queryset = JobAdvertisement.objects.all()
        # سریالایز کردن لیست آگهی‌های کارفرما
        serializer = JobAdvertisementSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, slug):
        # واکشی آگهی کارفرما بر مبنای آگهی عمومی (Advertisement) که اسلاگ آن برابر slug است.
        query = get_object_or_404(JobAdvertisement, advertisement__slug=slug)
        serializer = JobAdvertisementSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, slug):
        # بررسی می‌شود که کاربر دارای نوع کاربری (user_type) "EM" (کارفرما) است.
        if request.user.user_type == "EM":
            # ایجاد سریالایزر با داده‌های ورودی؛ در context، company_slug برابر با slug و request ارسال می‌شود
            serializer = JobAdvertisementSerializer(data=request.data, context={'company_slug': slug, 'request': request})
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
    
    def destroy(self, request, pk, slug):
        # واکشی آگهی عمومی مرتبط بر اساس slug
        main_ad = get_object_or_404(Advertisement, slug=slug)
        # واکشی آگهی کارفرما مرتبط که شناسه آن pk و فیلد advertisement برابر با main_ad باشد
        query = get_object_or_404(JobAdvertisement, id=pk, advertisement=main_ad)
        if query.advertisement.owner == request.user or request.user.is_staff:
            main_ad.delete()  # حذف آگهی عمومی از دیتابیس
            query.delete()    # حذف آگهی کارفرما
            return Response({"Massage": "The advertisement deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Massage": "You dont have the permissions."}, status=status.HTTP_403_FORBIDDEN)
        

# ======================================================================
# ResumeAdvertisementViewSet: ویوست جهت مدیریت آگهی‌های رزومه کارجو
# ======================================================================
class ResumeAdvertisementViewSet(viewsets.ViewSet):
    
    def list(self, request):
        # دریافت تمامی آگهی‌های رزومه کارجو
        queryset = ResumeAdvertisement.objects.all()
        serializer = ResumeAdvertisementSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, slug):
        # واکشی آگهی رزومه کارجو بر اساس اسلاگ آگهی عمومی (advertisement__slug)
        query = get_object_or_404(ResumeAdvertisement, advertisement__slug=slug)
        serializer = ResumeAdvertisementSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        # بررسی می‌شود که کاربر دارای نوع کاربری "JS" (جوینده کار) است.
        if request.user.user_type == "JS":
            # واکشی پروفایل جوینده کار بر اساس کاربر درخواست‌دهنده
            profile = get_object_or_404(JobSeekerProfile, user=request.user)
            # ایجاد سریالایزر جهت ایجاد آگهی رزومه؛ context شامل شناسه پروفایل و request ارسال می‌شود
            serializer = ResumeAdvertisementSerializer(data=request.data, context={'jobseeker_profile_id': profile.id, 'request': request})
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
    
    def destroy(self, request, pk, slug):
        # واکشی آگهی عمومی بر اساس slug
        main_ad = get_object_or_404(Advertisement, slug=slug)
        # واکشی آگهی رزومه کارجو مرتبط بر اساس شناسه (pk) و آگهی مربوطه (main_ad)
        query = get_object_or_404(ResumeAdvertisement, id=pk, advertisement=main_ad)
        if query.advertisement.owner == request.user or request.user.is_staff:
            main_ad.delete()  # حذف آگهی عمومی از دیتابیس
            query.delete()    # حذف آگهی رزومه کارجو
            return Response({"Massage": "The advertisement deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Massage": "You dont have the permissions."}, status=status.HTTP_403_FORBIDDEN)


# ======================================================================
# ApplicationViewSet: ویوست مدیریت درخواست‌های ارسال شده (Application)
# ======================================================================
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
