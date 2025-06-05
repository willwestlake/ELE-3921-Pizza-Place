from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('profile/', views.profile_view, name='profile'),
    path('reorder/', views.reorder_view, name='reorder'),


]
