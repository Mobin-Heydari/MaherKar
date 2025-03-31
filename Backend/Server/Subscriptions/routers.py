from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SubscriptionPlanViewSet,
    DurationViewSet,
    JobAdvertisementSubscriptionViewSet,
    JobseekerResumeAdvertisementSubscriptionViewSet,
)


class SubscriptionPlanRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', SubscriptionPlanViewSet, basename='subscription-plan')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', SubscriptionPlanViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', SubscriptionPlanViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls


class DurationRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', DurationViewSet, basename='duration')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', DurationViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', DurationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls


class JobAdvertisementSubscriptionRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', JobAdvertisementSubscriptionViewSet, basename='job-ad-subscription')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', JobAdvertisementSubscriptionViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', JobAdvertisementSubscriptionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls


class JobseekerResumeAdvertisementSubscriptionRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', JobseekerResumeAdvertisementSubscriptionViewSet, basename='resume-ad-subscription')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', JobseekerResumeAdvertisementSubscriptionViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', JobseekerResumeAdvertisementSubscriptionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls
