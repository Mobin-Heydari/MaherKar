from rest_framework import viewsets, permissions, status  # وارد کردن ویوست‌ها، مجوزها و وضعیت‌های HTTP
from rest_framework.response import Response  # کلاس Response جهت ارسال پاسخ به کلاینت
from rest_framework.generics import get_object_or_404  # تابع get_object_or_404 جهت بازیابی شیء یا ارسال خطای 404

# ایمپورت مدل‌های مورد استفاده در این ویوست‌ها
from .models import JobSeekerResume, Experience, Education, JobSeekerSkill
# ایمپورت سریالایزرهای مربوط به هر مدل
from .serializers import (
    JobSeekerResumeSerializer,
    ExperienceSerializer,
    EducationSerializer,
    JobSeekerSkillSerializer,
)

# ========================================
# JobSeekerResume ViewSet
# ========================================
class JobSeekerResumeViewSet(viewsets.ModelViewSet):
    """
    ویوست برای مدیریت عملیات مدل رزومه جوینده کار.
    این ویوست از ModelViewSet استفاده می‌کند تا عملیات CRUD (ایجاد، دریافت، به‌روزرسانی، حذف) را پیاده‌سازی کند.
    """
    queryset = JobSeekerResume.objects.all()                      # مجموعه رزومه‌های جوینده کار را از دیتابیس دریافت می‌کند
    serializer_class = JobSeekerResumeSerializer                    # استفاده از سریالایزر مربوط به رزومه جوینده کار
    permission_classes = [permissions.IsAuthenticated]              # تنها کاربران احراز هویت شده مجاز به دسترسی هستند

    def list(self, request, *args, **kwargs):
        # دریافت تمام رزومه‌ها و ارسال پاسخ در قالب JSON
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        # دریافت یک رزومه بر اساس شناسه (pk)؛ در صورت عدم وجود، خطای 404 ارسال می‌شود
        queryset = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # ایجاد رزومه جدید؛ داده‌های دریافتی توسط سریالایزر اعتبارسنجی شده و در صورت موفقیت ذخیره می‌شود
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # عملیات ذخیره که در سریالایزر، لینک کردن به job_seeker_profilehandled می‌شود.
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        # به‌روزرسانی یک رزومه موجود؛ از partial=True استفاده می‌شود تا امکان به‌روزرسانی جزئی فراهم شود
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        # حذف رزومه موجود؛ در صورت موفق، پیام حذف با وضعیت 204 ارسال می‌شود
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        instance.delete()
        return Response({"detail": "رزومه با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)


# ========================================
# Experience ViewSet
# ========================================
class ExperienceViewSet(viewsets.ModelViewSet):
    """
    ویوست برای مدیریت عملیات مدل تجربیات کاری رزومه.
    این ویوست امکان ایجاد، دریافت، به‌روزرسانی و حذف تجربیات کاری را فراهم می‌کند.
    """
    queryset = Experience.objects.all()             # دریافت تمام نمونه‌های Experience از دیتابیس
    serializer_class = ExperienceSerializer           # استفاده از سریالایزر مربوط به مدل Experience
    permission_classes = [permissions.IsAuthenticated]# تنها کاربران احراز هویت شده مجاز هستند

    def list(self, request, *args, **kwargs):
        # دریافت لیست تمام تجربیات کاری
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        # دریافت یک تجربه کاری بر اساس شناسه (pk)
        item = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # ایجاد یک تجربه کاری جدید؛ ابتدا بررسی می‌شود که resume_id ارسال شده باشد
        resume_id = request.data.get('resume_id')
        if not resume_id:
            return Response({"error": "شناسه رزومه الزامی است."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # اطمینان از وجود رزومه با شناسه داده شده
            resume = JobSeekerResume.objects.get(id=resume_id)
            request.data['resume'] = resume.id  # افزودن شناسه رزومه به داده‌های ورودی
        except JobSeekerResume.DoesNotExist:
            return Response({"error": "رزومه یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        # به‌روزرسانی یک تجربه کاری موجود به صورت جزئی
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        # حذف تجربه کاری؛ در صورت موفقیت پیام حذف ارسال می‌شود
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        instance.delete()
        return Response({"detail": "تجربه کاری با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)


# ========================================
# Education ViewSet
# ========================================
class EducationViewSet(viewsets.ModelViewSet):
    """
    ویوست برای مدیریت عملیات مدل تحصیلات رزومه.
    این ویوست امکان ایجاد، دریافت، به‌روزرسانی و حذف تحصیلات را فراهم می‌کند.
    """
    queryset = Education.objects.all()              # دریافت تمام نمونه‌های Education
    serializer_class = EducationSerializer            # استفاده از سریالایزر مربوط به مدل Education
    permission_classes = [permissions.IsAuthenticated]# فقط کاربران احراز هویت شده مجاز هستند

    def list(self, request, *args, **kwargs):
        # دریافت لیست تمام تحصیلات
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        # دریافت یک تحصیلات بر اساس شناسه (pk)
        item = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # ایجاد تحصیلات جدید؛ ابتدا بررسی می‌شود که resume_id ارسال شده باشد
        resume_id = request.data.get('resume_id')
        if not resume_id:
            return Response({"error": "شناسه رزومه الزامی است."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # بررسی وجود رزومه با شناسه موردنظر
            resume = JobSeekerResume.objects.get(id=resume_id)
            request.data['resume'] = resume.id
        except JobSeekerResume.DoesNotExist:
            return Response({"error": "رزومه یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        # به‌روزرسانی تحصیلات موجود به صورت جزئی
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        # حذف تحصیلات موجود؛ پیام حذف موفقیت‌آمیز ارسال می‌شود
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        instance.delete()
        return Response({"detail": "تحصیلات با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)


# ========================================
# JobSeekerSkill ViewSet
# ========================================
class JobSeekerSkillViewSet(viewsets.ModelViewSet):
    """
    ویوست برای مدیریت عملیات مدل مهارت‌های رزومه جوینده کار.
    این ویوست امکان ایجاد، دریافت، به‌روزرسانی و حذف مهارت‌ها را فراهم می‌کند.
    """
    queryset = JobSeekerSkill.objects.all()         # دریافت تمام نمونه‌های JobSeekerSkill
    serializer_class = JobSeekerSkillSerializer         # استفاده از سریالایزر مربوطه
    permission_classes = [permissions.IsAuthenticated]  # تنها کاربران احراز هویت شده دسترسی دارند

    def list(self, request, *args, **kwargs):
        # دریافت لیست کلیه مهارت‌های رزومه جوینده کار
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        # دریافت اطلاعات یک مهارت بر اساس شناسه (pk)
        item = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # ایجاد یک مهارت جدید؛ ابتدا بررسی می‌شود که resume_id ارسال شده باشد
        resume_id = request.data.get('resume_id')
        if not resume_id:
            return Response({"error": "شناسه رزومه الزامی است."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # بررسی وجود رزومه
            resume = JobSeekerResume.objects.get(id=resume_id)
            request.data['resume'] = resume.id
        except JobSeekerResume.DoesNotExist:
            return Response({"error": "رزومه یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        # به‌روزرسانی مهارت موجود با پشتیبانی از به‌روزرسانی جزئی
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        # حذف یک مهارت موجود؛ پیام حذف موفقیت‌آمیز ارسال می‌شود
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        instance.delete()
        return Response({"detail": "مهارت با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)
