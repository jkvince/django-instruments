from django.urls import path
from . import views
from .views import MainPageView, ProductCreateView

app_name = 'shop'

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('search/', views.prod_list, name='all_products'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('product/new/', ProductCreateView.as_view(), name='new_product'),  # Add a comma here
    path('<slug:category_slug>/', views.prod_list, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]
