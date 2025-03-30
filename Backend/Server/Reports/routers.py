from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JobSeekerReportViewSet,
    EmployerReportViewSet,
    AdminReportViewSet,
    SupportReportViewSet,
    AdvertisementReportViewSet,
    ResumeReportViewSet,
)


class JobSeekerReportRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'jobseeker-reports', JobSeekerReportViewSet, basename='jobseeker-report')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('jobseeker-reports/', include([
                path('', JobSeekerReportViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:id>/', JobSeekerReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls


class EmployerReportRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'employer-reports', EmployerReportViewSet, basename='employer-report')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('employer-reports/', include([
                path('', EmployerReportViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:id>/', EmployerReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls


class AdminReportRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'admin-reports', AdminReportViewSet, basename='admin-report')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('admin-reports/', include([
                path('', AdminReportViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:id>/', AdminReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls


class SupportReportRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'support-reports', SupportReportViewSet, basename='support-report')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('support-reports/', include([
                path('', SupportReportViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:id>/', SupportReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls


class AdvertisementReportRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'advertisement-reports', AdvertisementReportViewSet, basename='advertisement-report')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('advertisement-reports/', include([
                path('', AdvertisementReportViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:id>/', AdvertisementReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls


class ResumeReportRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'resume-reports', ResumeReportViewSet, basename='resume-report')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('resume-reports/', include([
                path('', ResumeReportViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:id>/', ResumeReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return urls + custom_urls
