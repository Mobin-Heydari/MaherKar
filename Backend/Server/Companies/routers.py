from rest_framework.routers import DefaultRouter  # وارد کردن کلاس DefaultRouter از Django REST Framework جهت ایجاد روتر سفارشی
from django.urls import path, include             # وارد کردن توابع path و include برای تعریف و درج URLها
from .views import CompanyViewSet                   # ایمپورت ویوست مربوط به شرکت (CompanyViewSet)

# تعریف یک روتر سفارشی برای مدیریت CompanyViewSet به همراه الگوهای URL اضافی
class CompanyRouter(DefaultRouter):
    """
    روتر سفارشی برای مدیریت CompanyViewSet با الگوهای URL اضافه.
    """
    def __init__(self):
        # فراخوانی سازنده‌ی کلاس والد (DefaultRouter)
        super().__init__()
        # ثبت CompanyViewSet در روتر با مسیر پایه (prefix خالی) و تعیین basename 'company'
        self.register(r'', CompanyViewSet, basename='company')

    def get_urls(self):
        """
        گسترش URLهای پیش‌فرض با الگوهای سفارشی در صورت نیاز.
        """
        # دریافت URLهای پیش‌فرض تعریف شده توسط کلاس والد
        urls = super().get_urls()

        # تعریف URLهای سفارشی برای CompanyViewSet
        custom_urls = [
            path('', include([
                # مسیر خالی برای فراخوانی متد list ویوست (دریافت لیست شرکت‌ها) از طریق متد GET
                path('', CompanyViewSet.as_view({'get': 'list'})),
                # مسیر خالی برای فراخوانی متد create ویوست (ایجاد شرکت جدید) از طریق متد POST
                path('', CompanyViewSet.as_view({'post': 'create'})),
                # مسیر شامل یک پارامتر رشته‌ای (pk) برای عملیات دریافت و به‌روزرسانی یک شرکت خاص
                path('<uuid:pk>/', include([
                    # فراخوانی متد retrieve جهت دریافت اطلاعات یک شرکت (به وسیله GET)
                    path('', CompanyViewSet.as_view({'get': 'retrieve'})),
                    # فراخوانی متد update جهت به‌روزرسانی اطلاعات شرکت (به وسیله PUT)
                    path('', CompanyViewSet.as_view({'put': 'update'})),
                ])),
            ])),
        ]
        # ترکیب URLهای پیش‌فرض و سفارشی و بازگرداندن کل مجموعه URLها
        return custom_urls
