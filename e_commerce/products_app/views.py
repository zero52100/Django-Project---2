from django.shortcuts import render, redirect
from .forms import ProductForm, ProductImageFormset
from .models import Product,ProductImage
from decimal import Decimal
from django.contrib import messages
from cart.models import Cart, CartItem
from django.urls import reverse

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormset(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()
            messages.success(request,"Prodcut added Sucessfully")
            return redirect('home') 
    else:
        form = ProductForm()
        formset = ProductImageFormset()
    return render(request, 'products_app/add_product.html', {'form': form, 'formset': formset})
def view_product(request):
    Product_list=Product.objects.all()
    for product in Product_list:
        # Calculate discounted price
        discounted_price = product.price - (product.price * product.discount_percentage / Decimal(100))
        # Update product object with discounted price
        product.discounted_price = discounted_price
    return render(request, 'products_app/view_product.html',{'product_list':Product_list})
def edit(request, pk):
    product = Product.objects.get(id=pk)
    images = product.images.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormset(request.POST, request.FILES, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request,"Prodcut details changed Sucessfully")
            return redirect(reverse('view_product'))
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormset(instance=product)
    context = {'form': form, 'formset': formset, 'product': product, 'images': images}
    return render(request, 'products_app/edit_product.html', context)
def delete(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    messages.success(request,"Prodcut deleted Sucessfully")
    return redirect(reverse('view_product'))  
def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    product_images = ProductImage.objects.filter(product=product)
    
    discounted_price = product.price - (product.price * product.discount_percentage / Decimal(100))
    
    product.discounted_price = discounted_price
    
    return render(request, 'products_app/product_detail.html', {'product': product, 'product_images': product_images})
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    if product.available_quantity >=1 :
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
        
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request,"Cart updated")
    else:
            messages.error(request,"Out of stock")


    return redirect('view_cart')




