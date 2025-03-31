from rest_framework import routers
from django.urls import path, include
from Advertisements.views import JobAdvertisementViewSet, ApplicationViewSet, JobseekerResumeAdvertisementViewSet



class JobAdvertisementRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', JobAdvertisementViewSet, basename='job-advertisements')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', JobAdvertisementViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<slug:slug>/', include([
                    path('', JobAdvertisementViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
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


class JobseekerResumeAdvertisementRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', JobseekerResumeAdvertisementViewSet, basename='applications')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', JobseekerResumeAdvertisementViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<slug:slug>/', include([
                    path('', JobseekerResumeAdvertisementViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
                ])),
            ])),
        ]
        return urls + custom_urls
