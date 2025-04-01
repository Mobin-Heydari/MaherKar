# urls.py
from django.urls import path, include
from .routers import ProvinceRouter, CityRouter



app_name = "Locations" 

province_router = ProvinceRouter()
city_router = CityRouter()

urlpatterns = [
    path('provinces/', include(province_router.urls)),
    path('cities/', include(city_router.urls)),
]
