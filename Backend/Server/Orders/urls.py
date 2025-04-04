# urls.py
from django.urls import path, include
from .routers import SubscriptionOrderRouter



app_name = "Locations" 

sub_orders = SubscriptionOrderRouter()

urlpatterns = [
    path('subscription-orders/', include(sub_orders.urls)),
]
