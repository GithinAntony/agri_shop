from django.urls import path
from . import views

app_name='index'
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('blog', views.blog, name='blog'),
    path('contact-us', views.contact_us, name='contact_us'),
    ]
