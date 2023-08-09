from django.urls import path
from . import views

app_name='farmer'
urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('list-products', views.products_list, name="products_list"),
    path('add-products', views.products_add, name="products_add"),
    path('delete-products/<int:id>', views.delete_products, name="delete_products"),
    path('view-product/<int:id>', views.products_view, name="products_view"),
]
