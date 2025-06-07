from django.urls import path, include
from .routers import SubscriptionOrderRouter




app_name = "Orders"




sub_orders = SubscriptionOrderRouter()


urlpatterns = [
    path('subscriptions/', include(sub_orders.urls)),
]
