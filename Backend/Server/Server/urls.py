from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('Users.urls', namespace='User')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
