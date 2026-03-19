from django.urls import path

from . import views

urlpatterns = [
    path('',views.product,name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('increase/<int:cart_id>/', views.increase_quantity, name='increase'),
    path('decrease/<int:cart_id>/', views.decrease_quantity, name='decrease'),
    path('remove/<int:cart_id>/', views.remove_item, name='remove'),
    path('register', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path("logout/", views.logout_view, name="logout"),
    ]