from rest_framework import routers
from django.urls import path, include
from Advertisements.views import AdvertisementViewSet, ApplicationViewSet




class AdvertisementRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', AdvertisementViewSet, basename='Advertisements')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', AdvertisementViewSet.as_view({'get': 'list'})),
                path('<slug:slug>/', include([
                    path('', AdvertisementViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
                ])),
            ])),
        ]
        return urls + custom_urls


class ApplicationRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', ApplicationViewSet, basename='applications')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', ApplicationViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', include([
                    path('', ApplicationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
                ])),
            ])),
        ]
        return urls + custom_urls
