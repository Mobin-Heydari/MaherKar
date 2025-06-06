from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CompanyViewSet



class CompanyRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', CompanyViewSet, basename='company')

    def get_urls(self):

        custom_urls = [
            path('', include([
                path('', CompanyViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<uuid:pk>/', include([
                    path('', CompanyViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
                ])),
            ])),
        ]
        return custom_urls