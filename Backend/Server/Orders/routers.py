from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import SubscriptionOrderViewSet



class SubscriptionOrderRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        # Register SubscriptionOrderViewSet with an empty prefix so we can define custom URLs.
        self.register(r'', SubscriptionOrderViewSet, basename='SubscriptionOrder')

    def get_urls(self):
        # Fetch default URLs (if any)
        urls = super().get_urls()
        # Define custom URL patterns using slug as the lookup field.
        custom_urls = [
            path('', include([
                path('', SubscriptionOrderViewSet.as_view({'get': 'list'})),
                path('<str:order_id>/', SubscriptionOrderViewSet.as_view({'get': 'retreive'})),
                path('<int:plan_id>/<int:subscription_id>/<slug:ad_slug>/', SubscriptionOrderViewSet.as_view({'post': 'create'})),
            ])),
        ]
        return urls + custom_urls