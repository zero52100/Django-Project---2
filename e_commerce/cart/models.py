from django.db import models
from django.contrib.auth import get_user_model
from products_app.models import Product

User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_cart_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def update_total_cart_value(self):
        cart_items = self.cartitem_set.all()
        total_value = sum(item.total_price for item in cart_items)
        self.total_cart_value = total_value
        self.save()

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)  # Provide a default value of None
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_total_price(self):
        if self.product.discount_percentage != 0:
            discounted_price = self.product.price - (self.product.price * self.product.discount_percentage / 100)
            self.total_price = discounted_price * self.quantity
        else:
            self.total_price = self.product.price * self.quantity

    def save(self, *args, **kwargs):
        if self.user_id is None:
            self.user = self.cart.user  # Assign the user from the associated cart
        self.calculate_total_price()
        super().save(*args, **kwargs)
        self.cart.update_total_cart_value()
class PaymentMethod(models.Model):
    PAYMENT_CHOICES = [
        ('debit_card', 'Debit Card'),
        ('upi', 'UPI'),
    ]

    
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    

    def __str__(self):
        return f"{self.user.username}'s Payment Method"
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    order_status = models.CharField(max_length=20)
    order_date = models.DateTimeField(auto_now_add=True)
    
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=0) 
    quantity = models.PositiveIntegerField()