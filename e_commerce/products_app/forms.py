from django import forms
from .models import Product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['brand_name', 'Product_name', 'description', 'price', 'thumbnail', 'category', 'available_quantity', 'discount_percentage', 'weight', 'weight_unit',  'expiry_date']

ProductImageFormset = forms.inlineformset_factory(
    Product,
    ProductImage,
    fields=('image',),
    extra=3
)
