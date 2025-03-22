from django.urls import path
from . import views


app_name = "Authentication"


urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name="login"),

    # Registeration OTP
    path('register-otp/', views.UserRegisterOtpAPIView.as_view(), name="user_register_otp"),
    path('register-otp-validate/<str:token>/', views.UserRegisterOtpValidateAPIView.as_view(), name="user_register_otp_validate"),
]