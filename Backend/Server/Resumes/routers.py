from rest_framework import routers
from django.urls import path, include
from .views import (
    JobSeekerResumeViewSet,
    ExperienceViewSet,
    EducationViewSet,
    JobSeekerSkillViewSet,
)


# JobSeekerResume Router
class JobSeekerResumeRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', JobSeekerResumeViewSet, basename='job-seeker-resumes')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', JobSeekerResumeViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', include([
                    path('', JobSeekerResumeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
                ])),
            ])),
        ]
        return urls + custom_urls


# Experience Router
class ExperienceRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', ExperienceViewSet, basename='experiences')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', ExperienceViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', include([
                    path('', ExperienceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
                ])),
            ])),
        ]
        return urls + custom_urls


# Education Router
class EducationRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', EducationViewSet, basename='educations')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', EducationViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', include([
                    path('', EducationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
                ])),
            ])),
        ]
        return urls + custom_urls


# JobSeekerSkill Router
class JobSeekerSkillRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', JobSeekerSkillViewSet, basename='skills')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', JobSeekerSkillViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', include([
                    path('', JobSeekerSkillViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
                ])),
            ])),
        ]
        return urls + custom_urls
