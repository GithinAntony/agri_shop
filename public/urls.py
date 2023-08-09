from django.urls import path
from . import views

app_name='public'
urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('header-search-item', views.header_search_item, name="header_search_item"),
    path('shop', views.shop, name="shop"),
    path('shop-details/<int:id>', views.shop_details, name="shop_details"),
    path('shop-cart', views.shop_cart, name="shop_cart"),
    path('shop-cart-delete/<int:id>', views.shop_cart_delete, name="shop_cart_delete"),
    path('shop-checkout', views.shop_checkout, name="shop_checkout"),
    path('shop-checkout-order', views.shop_checkout_order, name="shop_checkout_order"),       
 ]
