# ایمپورت ماژول‌های مورد نیاز
from rest_framework import routers
from django.urls import path, include

from .views import UserViewSet, IdCardViewSet



class IdCardRouter(routers.DefaultRouter):
    # مقداردهی اولیه روت سفارشی
    def __init__(self):
        super().__init__()
        self.register(r'', IdCardViewSet, basename='users')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', IdCardViewSet.as_view({'get': 'list'})),
                path('<int:pk>/', include([
                    path('', IdCardViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
                ])),
            ])),
        ]
        return urls + custom_urls
    

# تعریف یک کلاس روت سفارشی
class UserRouter(routers.DefaultRouter):
    # مقداردهی اولیه روت سفارشی
    def __init__(self):
        super().__init__()
        # ثبت ویوست UserViewSet در این روت سفارشی
        self.register(r'', UserViewSet, basename='users')

    # تعریف یک متد برای دریافت URLهای سفارشی
    def get_urls(self):
        # دریافت URLها از کلاس والد
        urls = super().get_urls()
        # تعریف URLهای سفارشی برای UserViewSet
        custom_urls = [
            # تعریف یک الگوی URL برای نمایش لیست
            path('', include([
                # تعریف یک الگوی URL برای نمایش لیست کاربران
                path('', UserViewSet.as_view({'get': 'list'})),
                # تعریف یک الگوی URL برای مشاهده جزئیات یک کاربر خاص
                path('<str:username>/', include([
                    # تعریف یک الگوی URL برای مشاهده جزئیات
                    path('', UserViewSet.as_view({'get': 'retrieve'})),
                ])),
            ])),
        ]
        # بازگشت URLهای سفارشی به علاوه URLهای اولیه
        return urls + custom_urls
