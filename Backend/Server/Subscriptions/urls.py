from django.urls import path, include
from .routers import  SubscriptionPlanRouter, AdvertisementSubscriptionRouter


app_name = "Subscriptions"


subscription_plan_router = SubscriptionPlanRouter()
ad_subscription_router = AdvertisementSubscriptionRouter()



urlpatterns = [
    path('plans/', include(subscription_plan_router.get_urls())),
    path('advertisement-subscription/', include(ad_subscription_router.get_urls()))
]
