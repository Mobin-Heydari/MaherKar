from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JobSeekerReportViewSet,
    EmployerReportViewSet,
    AdminReportViewSet,
    SupportReportViewSet,
    JobAdvertisementReportViewSet,
    ResumeAdvertisementReportViewSet,
)


class JobSeekerReportRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', JobSeekerReportViewSet, basename='jobseeker-report')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', JobSeekerReportViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:id>/', JobSeekerReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls


class EmployerReportRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', EmployerReportViewSet, basename='employer-report')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', EmployerReportViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:id>/', EmployerReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls


class AdminReportRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', AdminReportViewSet, basename='admin-report')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', AdminReportViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:id>/', AdminReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls


class SupportReportRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', SupportReportViewSet, basename='support-report')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', SupportReportViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:id>/', SupportReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls


class JobAdvertisementReportRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', JobAdvertisementReportViewSet, basename='advertisement-report')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', JobAdvertisementReportViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:id>/', JobAdvertisementReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls


class ResumeAdvertisementReportRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', ResumeAdvertisementReportViewSet, basename='resume-report')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', ResumeAdvertisementReportViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:id>/', ResumeAdvertisementReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls
