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
        # تعریف الگوهای URL سفارشی با استفاده از فیلد pk به عنوان شناسه (lookup_field)
        custom_urls = [
            path('', include([
                # مسیر خالی: اختصاص متد list (GET) و create (POST) برای استان‌ها
                path('', ProvinceViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر شامل پارامتر pk برای عملیات دریافت (retrieve)، به‌روزرسانی (PUT) و حذف (DELETE)
                path('<int:pk>/', include([
                    path('', ProvinceViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        # ترکیب URLهای پیش‌فرض و الگوهای سفارشی و بازگردانی مجموعه نهایی URLها
        return custom_urls


# -----------------------------------------------------------
# روتر شهر (CityRouter)
# -----------------------------------------------------------
class CityRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # ثبت ویوست CityViewSet با prefix خالی برای امکان تعریف URLهای سفارشی
        self.register(r'', CityViewSet, basename='city')

    def get_urls(self):
        custom_urls = [
            path('', include([
                # مسیر خالی: اختصاص متد list (GET) برای دریافت لیست شهرها
                path('', CityViewSet.as_view({'get': 'list', 'post': 'create'})),
                # مسیر جزئیات شهر: استفاده از pk شهر برای دریافت (GET)، به‌روزرسانی (PUT) و حذف (DELETE)
                path('<int:pk>/', include([
                    path('', CityViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return custom_urls