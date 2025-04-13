from django.shortcuts import get_object_or_404  # برای دریافت شی از دیتابیس و ارسال خطای 404 در صورت عدم وجود
from rest_framework import viewsets, status   # وارد کردن viewsets جهت استفاده از قابلیت‌های CRUD و status جهت تعریف کدهای HTTP
from rest_framework.response import Response     # کلاس پاسخ جهت ارسال داده‌ها به کلاینت
from rest_framework.exceptions import PermissionDenied  # برای رد درخواست‌های بدون مجوز

from .permissions import IsAdminUserOrReadOnly  # ایمپورت کلاس مجوز سفارشی؛ در اینجا تنها ادمین اجازه‌ی ایجاد، ویرایش و حذف دارند
from .models import Province, City             # ایمپورت مدل‌های Province و City از فایل models
from .serializers import ProvinceSerializer, CitySerializer  # ایمپورت سریالایزرهای مرتبط



# -------------------------------------------------------------
# ViewSet استان (ProvinceViewSet)
# -------------------------------------------------------------
class ProvinceViewSet(viewsets.ViewSet):
    """
    ویوست جهت لیست، دریافت، ایجاد، به‌روزرسانی و حذف نمونه‌های مدل Province.
    تنها کاربران ادمین (staff) می‌توانند عملیاتی نظیر ایجاد، به‌روزرسانی یا حذف انجام دهند.
    """
    # تعیین کلاس‌های مجوز جهت دسترسی؛ در اینجا IsAdminUserOrReadOnly اجازه‌ی انجام تغییرات تنها به admin می‌دهد
    permission_classes = [IsAdminUserOrReadOnly]

    def list(self, request):
        # دریافت تمامی استان‌ها از دیتابیس
        provinces = Province.objects.all()
        # سریالایز کردن داده‌ها؛ many=True به این معناست که لیست از نمونه‌ها ارسال می‌شود
        serializer = ProvinceSerializer(provinces, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug):
        # دریافت یک استان بر اساس اسلاگ؛ در صورت عدم وجود، 404 برگردانده می‌شود
        province = get_object_or_404(Province, slug=slug)
        serializer = ProvinceSerializer(province)
        return Response(serializer.data)

    def create(self, request):
        # تنها در صورتی که کاربر admin (is_staff=True) باشد، اجازه ایجاد داده دارد.
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can create data.")
        # ساختن نمونه سریالایزر از داده‌های دریافتی
        serializer = ProvinceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # فراخوانی متد create() سریالایزر برای ایجاد نمونه جدید
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # در صورت بروز خطا در اعتبارسنجی، ارسال خطاهای دریافتی با کد 400
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug):
        # تنها ادمین اجازه به‌روزرسانی دارند؛ در غیر این صورت، درخواست رد می‌شود.
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can update data.")
        # دریافت نمونه استان بر اساس slug
        province = get_object_or_404(Province, slug=slug)
        # ساختن سریالایزر برای به‌روزرسانی نمونه با داده‌های جدید
        serializer = ProvinceSerializer(province, data=request.data)
        if serializer.is_valid():
            serializer.save()  # فراخوانی متد update() سریالایزر جهت به‌روزرسانی نمونه
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug):
        # تنها admin مجاز به حذف داده‌هاست؛ در غیر این صورت، درخواست باعث خطای PermissionDenied می‌شود.
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can delete data.")
        # بازیابی استان بر اساس slug
        province = get_object_or_404(Province, slug=slug)
        province.delete()  # حذف نمونه از دیتابیس
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------------------------------------------------
# ViewSet شهر (CityViewSet)
# -------------------------------------------------------------
class CityViewSet(viewsets.ViewSet):
    """
    ویوست جهت لیست، دریافت، ایجاد، به‌روزرسانی و حذف نمونه‌های مدل City.
    سریالایزر شهر انتظار دارد که در context، کلید 'province_slug' ارسال شود.
    تنها کاربران admin می‌توانند داده‌ها را تغییر دهند.
    """
    permission_classes = [IsAdminUserOrReadOnly]

    def list(self, request):
        # دریافت تمامی شهرها از دیتابیس
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug):
        # دریافت یک شهر بر اساس اسلاگ آن؛ در صورت عدم وجود، خطای 404 برگردانده می‌شود
        city = get_object_or_404(City, slug=slug)
        # ایجاد نمونه سریالایزر بدون context اضافی (در صورت نیاز می‌توان context اضافه کرد)
        serializer = CitySerializer(city, context={})
        return Response(serializer.data)

    def create(self, request, province_slug):
        # چک می‌کند که کاربر admin باشد؛ در غیر این صورت خطای PermissionDenied صادر می‌شود
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can create data.")
        # واکشی استان بر اساس province_slug از URL؛ در صورت عدم وجود استان خطای 404 صادر می‌شود
        province = get_object_or_404(Province, slug=province_slug)
        # ایجاد سریالایزر جدید برای City با انتقال context شامل province_slug
        serializer = CitySerializer(data=request.data, context={'province_slug': province.slug})
        if serializer.is_valid():
            serializer.save()  # فراخوانی متد create() سریالایزر جهت ایجاد نمونه جدید شهر
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug):
        # تنها admin مجاز به به‌روزرسانی داده‌هاست
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can update data.")
        # بازیابی شهر بر اساس اسلاگ
        city = get_object_or_404(City, slug=slug)
        # ایجاد سریالایزر به‌منظور به‌روزرسانی شهر؛ در context، مقدار province_slug (در صورت ارسال) گرفته می‌شود
        serializer = CitySerializer(
            city, 
            data=request.data, 
            context={'province_slug': request.data.get('province_slug')}
        )
        if serializer.is_valid():
            serializer.save()  # فراخوانی متد update() سریالایزر جهت به‌روزرسانی داده‌ها
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug):
        # تنها admin مجاز به حذف داده‌ها هستند
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can delete data.")
        # دریافت شهر با استفاده از اسلاگ؛ ارسال خطای 404 در صورت عدم وجود
        city = get_object_or_404(City, slug=slug)
        city.delete()  # حذف شهر از دیتابیس
        return Response(status=status.HTTP_204_NO_CONTENT)
