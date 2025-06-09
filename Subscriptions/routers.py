from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionPlanViewSet, AdvertisementSubscriptionViewSet




class SubscriptionPlanRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', SubscriptionPlanViewSet, basename='subscription-plan')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', SubscriptionPlanViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', SubscriptionPlanViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return custom_urls


class AdvertisementSubscriptionRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', AdvertisementSubscriptionViewSet, basename='job-ad-subscription')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', AdvertisementSubscriptionViewSet.as_view({'get': 'list'})),
                path('<int:pk>/', AdvertisementSubscriptionViewSet.as_view({'get': 'retrieve'})),
            ])),
        ]
        return custom_urls
