from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<slug:product_slug>/', views.add_cart, name='add_cart'),
    path('remove/<slug:product_slug>/', views.cart_remove, name='cart_remove'),
    path('full_remove/<slug:product_slug>/', views.full_remove, name='full_remove'),
    path('new_order/', views.create_order, name='new_order'),
]
