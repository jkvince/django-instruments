from django.db import models
import uuid
import os
from django.urls import reverse
# Slugify import + Link to source, Used to make product and category urls
# https://learndjango.com/tutorials/django-slug-tutorial
from django.utils.text import slugify

# Category 
class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField(blank = True)
    image = models.ImageField(upload_to = 'category', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:products_by_category', args=[self.slug])

    def __str__(self):
        return self.name
    
def product_image_upload_to(instance, filename):
    category_name = instance.category.name if instance.category else "uncategorized"
    category_folder = category_name.replace(" ","_").lower()
    upload_path = os.path.join('products', category_folder,filename)
    return upload_path
    
# Warhouse
class Warehouse(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=250, unique=True)
    location = models.CharField(max_length=250)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)

    class Meta:
        ordering = ('location',)
        verbose_name = 'warehouse'
        verbose_name_plural = 'warehouses'

    def __str__(self):
        return self.name

# Brands
class Brand(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='brands', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def __str__(self):
        return self.name 

# Products
class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to= product_image_upload_to, blank=True)
    stock = models.IntegerField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'
    
    # Save function for slugify
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.category.slug, self.slug])


    def __str__(self):
        return self.name

