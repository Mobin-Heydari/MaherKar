from django.shortcuts import get_object_or_404  # دریافت شیء از دیتابیس یا برگرداندن خطای 404 در صورت عدم وجود
from rest_framework.views import Response       # وارد کردن کلاس Response برای ارسال پاسخ‌های HTTP
from rest_framework.viewsets import ModelViewSet  # وارد کردن ModelViewSet جهت استفاده از امکانات CRUD
from rest_framework import status                 # وارد کردن وضعیت‌های HTTP مانند 200، 400، 201 و غیره
from rest_framework.permissions import IsAuthenticated  # برای محدود کردن دسترسی به کاربران احراز هویت شده
from .models import Company                        # ایمپورت مدل Company از همان اپلیکیشن
from .serializers import CompanySerializer         # ایمپورت سریالایزر مربوط به مدل Company
from .permissions import IsAdminOrOwnerForUpdateAndEmployerForCreate  # ایمپورت کلاس‌های مجوز سفارشی


class CompanyViewSet(ModelViewSet):
    """
    ویوست برای مدیریت عملیات روی مدل شرکت.
    این ویوست امکان ایجاد، مشاهده، به‌روزرسانی و حذف شرکت‌ها را فراهم می‌کند.
    """
    queryset = Company.objects.all()  # مجموعه تمامی نمونه‌های شرکت را بازیابی می‌کند
    serializer_class = CompanySerializer  # استفاده از CompanySerializer جهت تبدیل داده‌ها به JSON و بالعکس
    permission_classes = [IsAuthenticated, IsAdminOrOwnerForUpdateAndEmployerForCreate]
    # فقط کاربران احراز هویت شده و کسانی که مجوزهای اضافی (مدیر یا صاحب شرکت) دارند، قادر به انجام تغییرات هستند

    # استفاده از slug به عنوان شناسه جهت عملیات retrieve/update/delete
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        """List all companies.
           دریافت لیست تمامی شرکت‌ها.
        """
        queryset = self.get_queryset()  # دریافت queryset از متد پیش‌فرض
        serializer = self.get_serializer(queryset, many=True)  # سریالایز کردن داده‌ها در قالب لیست
        return Response(serializer.data, status=status.HTTP_200_OK)  # ارسال پاسخ موفقیت‌آمیز با کد 200

    def retrieve(self, request, slug, *args, **kwargs):
        """Retrieve a specific company by its slug.
           دریافت اطلاعات یک شرکت بر اساس اسلاگ (slug).
        """
        instance = get_object_or_404(Company, slug=slug)  # دریافت شرکت با استفاده از فیلد slug؛ اگر یافت نشود، خطای 404 صادر می‌شود
        serializer = self.get_serializer(instance)         # سریالایز کردن نمونه شرکت
        return Response(serializer.data, status=status.HTTP_200_OK)  # ارسال داده‌های سریالایز شده با وضعیت 200

    def create(self, request, *args, **kwargs):
        """Create a new company. Employer field is auto-assigned.
           ایجاد شرکت جدید؛ فیلد employer به‌صورت خودکار از کاربر درخواست‌کننده (request.user) اختصاص پیدا می‌کند.
        """
        serializer = self.get_serializer(data=request.data)  # ساختن سریالایزر با داده‌های دریافتی از درخواست
        if serializer.is_valid():  # صحت‌سنجی داده‌ها، در صورت درست بودن ادامه می‌دهد
            # فیلد employer با ارسال employer_id به متد save پر می‌شود؛ این employer_id از request.user.id گرفته می‌شود
            serializer.save(employer_id=request.user.id)
            # ارسال پیام موفقیت‌آمیز به همراه کد 201 (ایجاد موفق)
            return Response({'Message': 'Company created successfully.'}, status=status.HTTP_201_CREATED)
        # در صورت عدم اعتبارسنجی، خطاهای دریافت شده را با کد 400 برمی‌گرداند
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug, *args, **kwargs):
        """Update an existing company.
           به‌روزرسانی اطلاعات یک شرکت موجود بر اساس اسلاگ.
        """
        # تلاش برای دریافت شرکت بر اساس slug، در صورت عدم وجود خطای 404 برمی‌گرداند
        instance = get_object_or_404(Company, slug=slug)
        # استفاده از متد update سریالایزر؛ از partial=True استفاده شده تا امکان به‌روزرسانی جزئی (فیلدهای انتخابی) فراهم شود
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():  # صحت‌سنجی داده‌ها
            serializer.save()  # ذخیره تغییرات در دیتابیس
            return Response(serializer.data, status=status.HTTP_200_OK)  # ارسال داده‌های به‌روزرسانی شده با کد موفقیت‌آمیز 200
        # در صورت بروز خطا، خطاها با کد 400 برگردانده می‌شوند
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
