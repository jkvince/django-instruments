from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    model = Product
    template_name = "mainpage.html"
    context_object_name = "main_page"


class AboutPageView(TemplateView):
    template_name = 'about.html'
    context_object_name = "about"


def prod_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, available=True)
    
    paginator = Paginator(products, 6)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage,InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request, 'shop/category.html', {'category': category, 'products': products})
    

def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_slug)
    return render(request, 'shop/product.html', {'product': product})
