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
        self.register(r'subscription-plans', SubscriptionPlanViewSet, basename='subscription-plan')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('subscription-plans/', include([
                path('', SubscriptionPlanViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', SubscriptionPlanViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls


class DurationRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'durations', DurationViewSet, basename='duration')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('durations/', include([
                path('', DurationViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', DurationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls


class JobAdvertisementSubscriptionRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'job-ad-subscriptions', JobAdvertisementSubscriptionViewSet, basename='job-ad-subscription')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('job-ad-subscriptions/', include([
                path('', JobAdvertisementSubscriptionViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', JobAdvertisementSubscriptionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls


class JobseekerResumeAdvertisementSubscriptionRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'resume-ad-subscriptions', JobseekerResumeAdvertisementSubscriptionViewSet, basename='resume-ad-subscription')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('resume-ad-subscriptions/', include([
                path('', JobseekerResumeAdvertisementSubscriptionViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', JobseekerResumeAdvertisementSubscriptionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls
