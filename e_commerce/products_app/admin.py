from django.contrib import admin
from .models import Product, ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('Product_name', 'brand_name', 'category', 'price', 'available_quantity', 'discount_percentage', 'expiry_date')
    list_filter = ('category', 'expiry_date')
    search_fields = ('Product_name', 'brand_name')
    ordering = ('-expiry_date',)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
