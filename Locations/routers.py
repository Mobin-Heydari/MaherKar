from django.urls import path, include    # توابع path و include برای تعریف و درج URLها
from rest_framework import routers         # وارد کردن مدول روترهای DRF
from .views import ProvinceViewSet, CityViewSet   # ایمپورت ویوست‌های مربوط به استان و شهر



# -----------------------------------------------------------
# روتر استان (ProvinceRouter)
# -----------------------------------------------------------
class ProvinceRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت ویوست ProvinceViewSet با prefix خالی جهت تعریف URLهای سفارشی
        self.register(r'', ProvinceViewSet, basename='province')

    def get_urls(self):
        # دریافت URLهای پیش‌فرض موجود در DefaultRouter (در صورت تعریف)
        urls = super().get_urls()
        # تعریف الگوهای URL سفارشی با استفاده از فیلد slug به عنوان شناسه (lookup_field)
        custom_urls = [
            path('', include([
                # مسیر خالی: اختصاص متد list (GET) و create (POST) برای استان‌ها
                path('', ProvinceViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر شامل پارامتر slug برای عملیات دریافت (retrieve)، به‌روزرسانی (PUT) و حذف (DELETE)
                path('<slug:slug>/', include([
                    path('', ProvinceViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        # ترکیب URLهای پیش‌فرض و الگوهای سفارشی و بازگردانی مجموعه نهایی URLها
        return urls + custom_urls


# -----------------------------------------------------------
# روتر شهر (CityRouter)
# -----------------------------------------------------------
class CityRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت ویوست CityViewSet با prefix خالی برای امکان تعریف URLهای سفارشی
        self.register(r'', CityViewSet, basename='city')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                # مسیر خالی: اختصاص متد list (GET) برای دریافت لیست شهرها
                path('', CityViewSet.as_view({'get': 'list'})),
                # مسیر اختصاصی ایجاد شهر: دریافت شهر جدید با استفاده از پارامتر province_slug 
                # (این الگو به منظور ایجاد شهر برای یک استان خاص تعریف شده است)
                path('<slug:province_slug>', CityViewSet.as_view({'post': 'create'})),
                # مسیر جزئیات شهر: استفاده از slug شهر برای دریافت (GET)، به‌روزرسانی (PUT) و حذف (DELETE)
                path('<slug:slug>/', include([
                    path('', CityViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return urls + custom_urls