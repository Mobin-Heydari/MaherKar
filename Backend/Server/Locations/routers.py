# routers.py
from django.urls import path, include
from rest_framework import routers
from .views import ProvinceViewSet, CityViewSet

class ProvinceRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # Register ProvinceViewSet with an empty prefix so we can define custom URLs.
        self.register(r'', ProvinceViewSet, basename='province')

    def get_urls(self):
        # Fetch default URLs (if any)
        urls = super().get_urls()
        # Define custom URL patterns using slug as the lookup field.
        custom_urls = [
            path('', include([
                # For listing (GET) and creating (POST)
                path('', ProvinceViewSet.as_view({'get': 'list', 'post': 'create'})),
                # For detail endpoints: retrieve (GET), update (PUT), destroy (DELETE)
                path('<slug:slug>/', include([
                    path('', ProvinceViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return urls + custom_urls


class CityRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        # Register CityViewSet with an empty prefix for custom URL routing.
        self.register(r'', CityViewSet, basename='city')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                # URL patterns for listing (GET) and creating (POST) cities.
                path('', CityViewSet.as_view({'get': 'list', 'post': 'create'})),
                # URL patterns using the city's slug for detail views.
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
