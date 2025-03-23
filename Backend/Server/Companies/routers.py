from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CompanyViewSet





class CompanyRouter(DefaultRouter):
    """
    Custom router for managing CompanyViewSet with additional URL patterns.
    """
    def __init__(self):
        super().__init__()
        # Register the CompanyViewSet with the base path
        self.register(r'', CompanyViewSet, basename='company')

    def get_urls(self):
        """
        Extend default URLs with custom patterns if needed.
        """
        # Default URLs from the parent class
        urls = super().get_urls()

        # Define custom URLs for the CompanyViewSet
        custom_urls = [
            path('', include([
                path('', CompanyViewSet.as_view({'get': 'list'})),  # Custom URL for listing companies
                path('', CompanyViewSet.as_view({'post': 'create'})),  # Custom URL for creating companies
                path('<str:slug>/', include([  # Custom URL for retrieving a specific company
                    path('', CompanyViewSet.as_view({'get': 'retrieve'})),
                    path('', CompanyViewSet.as_view({'put': 'update'})),
                ])),
            ])),
        ]
        # Return the combined list of default and custom URLs
        return urls + custom_urls
