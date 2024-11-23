from django.contrib import admin
from .models import Category, Product, Warehouse

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Category, CategoryAdmin)

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['location']

admin.site.register(Warehouse, WarehouseAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'category', 'stock', 'available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    list_per_page = 20

admin.site.register(Product, ProductAdmin)