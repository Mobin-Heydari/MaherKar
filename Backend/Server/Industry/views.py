from django.shortcuts import get_object_or_404  # دریافت شیء از دیتابیس؛ در صورت عدم وجود با ارسال خطای 404
from rest_framework.views import Response       # کلاس پاسخ برای ارسال داده‌ها به کلاینت
from rest_framework.viewsets import ModelViewSet  # استفاده از ModelViewSet جهت فراهم‌سازی عملیات‌های CRUD
from rest_framework import status                 # وارد کردن حالات HTTP (مانند 200, 400, 403, 201, 204)
from rest_framework.permissions import IsAuthenticated  # محدود کردن دسترسی به کاربران احراز هویت شده

# ایمپورت مدل‌های مرتبط صنعت
from .models import IndustryCategory, Industry, Skill
# ایمپورت سریالایزرهای مربوط به مدل‌ها
from .serializers import IndustryCategorySerializer, IndustrySerializer, SkillSerializer




# =================================================
# ViewSet برای مدیریت دسته‌بندی‌های صنعت (IndustryCategory)
# =================================================
class IndustryCategoryViewSet(ModelViewSet):
    """
    ویوست برای مدیریت دسته‌بندی‌های صنعت.
    عملیات لیست، دریافت، ایجاد، به‌روزرسانی و حذف دسته‌بندی‌ها در این ویوست قابل انجام است.
    """
    queryset = IndustryCategory.objects.all()  # دریافت تمامی دسته‌بندی‌ها از دیتابیس
    # توجه: این خط به احتمال زیاد اشتباه است؛ در حال حاضر یک تاپل از دو سریالایزر دریافت شده است
    # بهتر است تنها از یک سریالایزر (مثلاً IndustryCategorySerializer) استفاده شود!
    serializer_class = IndustryCategorySerializer  
    permission_classes = [IsAuthenticated]  # فقط کاربران احراز هویت‌شده می‌توانند از این ویو استفاده کنند
    lookup_field = 'pk'  # استفاده از فیلد pk به عنوان شناسه در URL‌ها

    def list(self, request, *args, **kwargs):
        """لیست تمامی دسته‌بندی‌ها."""
        queryset = self.get_queryset()  # دریافت queryset از متد پیش‌فرض
        serializer = self.get_serializer(queryset, many=True)  # سریالایز کردن مجموعه دسته‌بندی‌ها
        return Response(serializer.data, status=status.HTTP_200_OK)  # ارسال پاسخ موفقیت‌آمیز

    def retrieve(self, request, pk, *args, **kwargs):
        """دریافت یک دسته‌بندی خاص بر اساس اسلاگ."""
        instance = get_object_or_404(IndustryCategory, id=pk)  # بازیابی دسته‌بندی با اسلاگ مشخص شده
        serializer = self.get_serializer(instance)  # سریالایز کردن نمونه دریافت شده
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """ایجاد یک دسته‌بندی جدید."""
        if request.user.is_staff:  # تنها کاربران ادمین (staff) مجاز به ایجاد دسته‌بندی هستند
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()  # ذخیره دسته‌بندی جدید
                return Response({'Message': 'Category created successfully.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Massage": "Only admin users can write datas"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk, *args, **kwargs):
        """به‌روزرسانی یک دسته‌بندی موجود."""
        if request.user.is_staff:
            instance = get_object_or_404(IndustryCategory, id=pk)  # دریافت دسته‌بندی جهت به‌روزرسانی
            serializer = self.get_serializer(instance=instance, data=request.data, partial=True)  # به‌روز‌رسانی جزئی
            if serializer.is_valid():
                serializer.save()  # ذخیره تغییرات
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Massage": "Only admin users can write datas"}, status=status.HTTP_403_FORBIDDEN)
        
    def destroy(self, request, pk):
        """حذف یک دسته‌بندی موجود."""
        if request.user.is_staff:
            category = get_object_or_404(IndustryCategory, id=pk)  # بازیابی دسته‌بندی بر اساس id
            self.perform_destroy(category)  # حذف دسته‌بندی
            return Response({"Massage": "The category deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Massage": "Only admin users can dele datas"}, status=status.HTTP_403_FORBIDDEN)


# =================================================
# ViewSet برای مدیریت صنایع (Industry)
# =================================================
class IndustryViewSet(ModelViewSet):
    """
    ویوست برای مدیریت صنایع.
    این ویوست امکان عملیات CRUD روی صنایع را فراهم می‌کند.
    """
    queryset = Industry.objects.all()  # دریافت تمامی صنایع از دیتابیس
    serializer_class = IndustrySerializer  # استفاده از سریالایزر مربوط به مدل Industry
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'  # استفاده از اسلاگ به عنوان شناسه در URL

    def list(self, request, *args, **kwargs):
        """لیست تمامی صنایع."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk, *args, **kwargs):
        """دریافت یک صنعت بر اساس اسلاگ."""
        instance = get_object_or_404(Industry, id=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        ایجاد یک صنعت جدید.
        این متد به یک پارامتر  نیاز دارد تا صنعت به یک دسته‌بندی مشخص متصل شود.
        """
        if request.user.is_staff:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()  # ذخیره صنعت جدید
                return Response({'Message': 'Industry created successfully.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Massage": "Only admin users can write datas"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk, *args, **kwargs):
        """به‌روزرسانی یک صنعت موجود."""
        if request.user.is_staff:
            instance = get_object_or_404(Industry, id=pk)
            serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()  # ذخیره به‌روزرسانی
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Massage": "Only admin users can write datas"}, status=status.HTTP_403_FORBIDDEN)
        
    def destroy(self, request, pk):
        """حذف صنعت موجود."""
        if request.user.is_staff:
            industry = get_object_or_404(Industry, id=pk)
            self.perform_destroy(industry)
            return Response({"Massage": "The industry deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Massage": "Only admin users can dele datas"}, status=status.HTTP_403_FORBIDDEN)


# =================================================
# ViewSet برای مدیریت مهارت‌ها (Skill)
# =================================================
class SkillViewSet(ModelViewSet):
    """
    ویوست برای مدیریت مهارت‌ها.
    این ویوست اجازه‌ی عملیات CRUD بر روی مهارت‌ها را می‌دهد.
    """
    queryset = Skill.objects.all()  # دریافت تمامی مهارت‌ها
    serializer_class = SkillSerializer  # سریالایزر مرتبط با مدل Skill
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'  # استفاده از فیلد pk به عنوان شناسه در URL؛ اگرچه در متدهای retrieve از pk استفاده شده است

    def list(self, request, *args, **kwargs):
        """لیست تمامی مهارت‌ها."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk, *args, **kwargs):
        """دریافت یک مهارت خاص بر اساس نام."""
        instance = get_object_or_404(Skill, id=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        ایجاد یک مهارت جدید.
        """
        if request.user.is_staff:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()  # ذخیره مهارت جدید
                return Response({'Message': 'Skill created successfully.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Massage": "Only admin users can write datas"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk, *args, **kwargs):
        """به‌روزرسانی یک مهارت موجود."""
        if request.user.is_staff:
            instance = get_object_or_404(Skill, id=pk)
            serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()  # ذخیره به‌روزرسانی مهارت
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Massage": "Only admin users can write datas"}, status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, pk):
        """حذف مهارتی موجود."""
        if request.user.is_staff:
            skill = get_object_or_404(Skill, id=pk)
            self.perform_destroy(skill)
            return Response({"Massage": "The skill deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Massage": "Only admin users can dele datas"}, status=status.HTTP_403_FORBIDDEN)