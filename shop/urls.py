from django.urls import path
from . import views
from .views import MainPageView

app_name = 'shop'

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('search', views.prod_list, name = 'all_products'),
    path('about', views.AboutPageView.as_view(), name='about'),
    path('<uuid:category_id>/', views.prod_list, name = 'products_by_category'),
    path('<uuid:category_id>/<uuid:product_id>/', views.product_detail, name = 'product_detail'),
]
