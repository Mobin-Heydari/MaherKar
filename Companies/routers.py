from rest_framework.routers import DefaultRouter  # وارد کردن کلاس DefaultRouter از Django REST Framework جهت ایجاد روتر سفارشی
from django.urls import path, include             # وارد کردن توابع path و include برای تعریف و درج URLها
from .views import CompanyViewSet                   # ایمپورت ویوست مربوط به شرکت (CompanyViewSet)



class CompanyRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', CompanyViewSet, basename='company')

    def get_urls(self):

        custom_urls = [
            path('', include([
                path('', CompanyViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<uuid:pk>/', include([
                    path('', CompanyViewSet.as_view({'get': 'retrieve'})),
                    path('', CompanyViewSet.as_view({'put': 'update'})),
                ])),
            ])),
        ]
        return custom_urls
