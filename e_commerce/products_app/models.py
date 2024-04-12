from django.db import models
from django.utils import timezone

class Product(models.Model):
    WEIGHT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('ml', 'Milliliter'),
        ('L', 'Liter'),
        ('pcs', 'Pieces'),
    ]

    
    CATEGORY = [
        ('staples', 'Staples'),
        ('snacks_&_beverages', 'Snacks and Beverages'),
        ('household_items', 'Household Items'),
        ('dairy_and_eggs', 'Dairy and Eggs'),
    ]

    brand_name = models.CharField(max_length=100)
    Product_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    images = models.ManyToManyField('ProductImage', related_name='products')
    thumbnail = models.ImageField(upload_to='media/thumbnails/')
    category = models.CharField(max_length=55, choices=CATEGORY)
    available_quantity = models.PositiveIntegerField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    weight_unit = models.CharField(max_length=10, choices=WEIGHT_CHOICES, default='kg')
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    expiry_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.Product_name



class ProductImage(models.Model):
    product = models.ForeignKey('products_app.Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/product_images/')

    def __str__(self):
        return f"Image for {self.product.Product_name}"
