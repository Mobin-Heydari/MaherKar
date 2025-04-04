from django.urls import path
from . import views


app_name = "Payments"


urlpatterns = [
    path('zarinpal-pay/<str:order_id>/', views.SendPaymentRequest.as_view()),
    path('zarinpal-verify/', views.VerifyPaymentRequest.as_view())
]