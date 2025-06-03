from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('Users.urls', namespace='Users')),
    path('profiles/', include('Profiles.urls', namespace='Profiles')),
    path('auth/', include('Authentication.urls', namespace='Authentication')),
    path('companies/', include('Companies.urls', namespace='Companies')),
    path('industries/', include('Industry.urls', namespace='Industry')),
    path('resumes/', include('Resumes.urls', namespace='Resumes')),
    path('ads/', include('Advertisements.urls', namespace='Advertisements')),
    path('reports/', include('Reports.urls', namespace='Reports')),
    path('subscriptions/', include('Subscriptions.urls', namespace='Subscriptions')),
    path('locations/', include('Locations.urls', namespace='Locations')),
    path('orders/', include('Orders.urls', namespace='Orders')),
    path('payments/', include('Payments.urls', namespace='Payments')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
