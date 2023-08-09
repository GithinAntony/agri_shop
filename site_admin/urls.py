from django.urls import path
from . import views

app_name='site_admin'
urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('add-location', views.add_location, name="add_location"),
    path('delete-location/<int:id>', views.delete_location, name="delete_location"),
    path('add-category', views.add_category, name="add_category"),
    path('delete-category/<int:id>', views.delete_category, name="delete_category"),
    path('list-public-user', views.list_public_user, name="list_public_user"),
    path('list-farmer-user', views.list_farmer_user, name="list_farmer_user"),
    path('list-products', views.list_products, name="list_products"),
]
