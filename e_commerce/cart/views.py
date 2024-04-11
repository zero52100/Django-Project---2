
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem

@login_required
def view_cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = cart.cartitem_set.all()
    return render(request, 'cart/cart.html', {'cart_items': cart_items})


