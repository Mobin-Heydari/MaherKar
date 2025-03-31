from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import IndustryViewSet, IndustryCategoryViewSet, SkillViewSet




class IndustryCategoryRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', IndustryCategoryViewSet, basename='industry-category')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', IndustryCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<slug:slug>/', IndustryCategoryViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
            ])),
        ]
        return urls + custom_urls



class IndustryRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', IndustryViewSet, basename='industry')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', IndustryViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<slug:slug>/', IndustryViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
            ])),
        ]
        return urls + custom_urls
    


class SkillRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', SkillViewSet, basename='skill')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', SkillViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<slug:slug>/', SkillViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
            ])),
        ]
        return urls + custom_urls
