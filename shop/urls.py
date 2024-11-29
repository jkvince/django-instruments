from django.urls import path
from . import views
from .views import MainPageView

app_name = 'shop'

urlpatterns = [
    # Main page view
    path('', views.MainPageView.as_view(), name='main_page'),

    # Search or list all products
    path('search', views.prod_list, name='all_products'),

    # About page view
    path('about', views.AboutPageView.as_view(), name='about'),

    # Products by category using slug
    path('<slug:category_slug>/', views.prod_list, name='products_by_category'),

    # Product detail page using slugs for both category and product
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]
