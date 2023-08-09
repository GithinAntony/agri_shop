from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('index.urls'),),
    path('public/',include('public.urls',namespace='public'),),
    path('farmer/',include('farmer.urls',namespace='farmer'),),
    path('admin2022/',include('site_admin.urls',namespace='site_admin'),)
] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
