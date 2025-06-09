from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReportCategoryViewSet,
    EmployerReportViewSet,
    JobSeekerReportViewSet,
    AdvertisementReportViewSet
)


class ReportCategoryRouter(DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', ReportCategoryViewSet, basename='report-categories')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', ReportCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', ReportCategoryViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}))
            ]))
        ]
        return custom_urls


class JobSeekerReportRouter(DefaultRouter):
    """روتر برای مدیریت URLهای گزارش‌های جویندگان کار."""
    def __init__(self):
        super().__init__()
        self.register(r'', JobSeekerReportViewSet, basename='jobseeker-report')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', JobSeekerReportViewSet.as_view({'get': 'list'})),
                path('create/<int:pk>/', JobSeekerReportViewSet.as_view({'post': 'create'})),
                path('detail/<int:pk>/', JobSeekerReportViewSet.as_view({'get': 'retrieve'})),
                path('update/<int:pk>/', JobSeekerReportViewSet.as_view({'put': 'update'})),
                path('delete/<int:pk>/', JobSeekerReportViewSet.as_view({'delete': 'destroy'})),
            ])),
        ]
        return custom_urls

class EmployerReportRouter(DefaultRouter):
    """روتر برای مدیریت URLهای گزارش‌های کارفرما."""
    def __init__(self):
        super().__init__()
        self.register(r'', EmployerReportViewSet, basename='employer-report')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', EmployerReportViewSet.as_view({'get': 'list'})),
                path('create/<int:pk>/', EmployerReportViewSet.as_view({'post': 'create'})),
                path('detail/<int:pk>/', EmployerReportViewSet.as_view({'get': 'retrieve'})),
                path('update/<int:pk>/', EmployerReportViewSet.as_view({'put': 'update'})),
                path('delete/<int:pk>/', EmployerReportViewSet.as_view({'delete': 'destroy'})),
            ])),
        ]
        return custom_urls

class AdvertisementReportRouter(DefaultRouter):
    """روتر برای مدیریت URLهای گزارش‌های آگهی."""
    def __init__(self):
        super().__init__()
        self.register(r'', AdvertisementReportViewSet, basename='advertisement-report')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', AdvertisementReportViewSet.as_view({'get': 'list'})),
                path('create/<uuid:pk>/', AdvertisementReportViewSet.as_view({'post': 'create'})),
                path('detail/<int:pk>/', AdvertisementReportViewSet.as_view({'get': 'retrieve'})),
                path('update/<int:pk>/', AdvertisementReportViewSet.as_view({'put': 'update'})),
                path('delete/<int:pk>/', AdvertisementReportViewSet.as_view({'delete': 'destroy'})),
            ])),
        ]
        return custom_urls
