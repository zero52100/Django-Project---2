from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem,PaymentMethod,Order, OrderItem
from django.contrib import messages
from .forms import CheckoutForm
from django.db import IntegrityError
from users.models import CustomUser
import stripe
from django.http import HttpResponse
from django.conf import settings
from products_app.models import Product
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def view_cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = cart.cartitem_set.all()
    
    
    for item in cart_items:
        if item.product.discount_percentage != 0:
            discounted_price = item.product.price - (item.product.price * item.product.discount_percentage / 100)
            item.total_price = discounted_price * item.quantity
        else:
            item.total_price = item.product.price * item.quantity
    
    
    overall_total = sum(item.total_price for item in cart_items)
    
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'overall_total': overall_total})


def increment_item(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    
    
    if cart_item.quantity < cart_item.product.available_quantity:
        cart_item.quantity += 1
        cart_item.save()
    else:
       messages.error(request, "Product quantity reached. Maximum quantity reached for this product.")
    
    return redirect('view_cart')

def decrement_item(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')

@login_required
def shipping_address(request):
    user = request.user
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                
                user.full_name = form.cleaned_data['full_name']
                user.address = form.cleaned_data['address']
                user.pincode = form.cleaned_data['pincode']
                user.save()  
                
                return redirect('payment') 
            except IntegrityError:
                
                form.add_error(None, 'An error occurred while updating your information. Please try again.')
    else:
        form = CheckoutForm(initial={'full_name': user.full_name, 'address': user.address, 'pincode': user.pincode})
    return render(request, 'cart/shipping_address.html', {'form': form})

@login_required
def checkout(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = cart.cartitem_set.all()

    overall_total = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                user.full_name = form.cleaned_data['full_name']
                user.address = form.cleaned_data['address']
                user.pincode = form.cleaned_data['pincode']
                user.save()

              
                return redirect('payment')
            except IntegrityError:
                form.add_error(None, 'An error occurred while updating your information. Please try again.')
    else:
        form = CheckoutForm(initial={'full_name': user.full_name, 'address': user.address, 'pincode': user.pincode})

    return render(request, 'cart/checkout.html', {'form': form, 'cart_items': cart_items, 'overall_total': overall_total})

@login_required
def payment(request):
    user = request.user

    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')
        payment_method_id = request.POST.get('payment_method_id')

        if payment_type:
           
            confirm = request.POST.get('confirm')

            if confirm == 'yes':
                try:
                    payment_method = PaymentMethod.objects.get(id=payment_method_id)
                except PaymentMethod.DoesNotExist:
                    return HttpResponse('Invalid payment method') 
            
                order = Order.objects.create(
                    user=user,
                    total_price=0,
                    payment_method=payment_method.payment_type,
                    order_status='Pending'
                )

               
                cart_items = CartItem.objects.filter(user=user)
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity
                    )

               
                cart_items.delete()

                return HttpResponse('Payment successful!')  
            elif confirm == 'no':
                return HttpResponse('Payment not confirmed')  
                return HttpResponse('Invalid confirmation')  

        else:
            return HttpResponse('Please select a payment method')  #
    return render(request, 'cart/payment.html')



def process_order(request):
    if request.method == 'POST':
        
        payment_type = request.POST.get('payment_type')

        if payment_type:
            try:
                
                user = request.user
                cart_items = user.cart.cartitem_set.all()

               
                total_price = sum(item.total_price for item in cart_items)

                
                order = Order.objects.create(
                    user=user,
                    total_price=total_price,
                    payment_method=payment_type,  
                    order_status='Pending'  
                )
                
                
                for cart_item in cart_items:
                    product = cart_item.product
                    product.available_quantity -= cart_item.quantity  
                    product.save() 
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=cart_item.quantity
                    )
                subject = 'Your order has been placed'
                html_message = render_to_string('cart/order_confirmation.html', {'order': order})
                plain_message = strip_tags(html_message)
                from_email = settings.EMAIL_HOST_USER
                to_email = [user.email]
                send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

                user.cart.cartitem_set.all().delete()
                return redirect('order')
            except Exception as e:
               
                messages.error(request, f"An error occurred: {e}")
                return redirect('payment')

    return redirect('payment')
@login_required
def order_admin(request):

    orders = Order.objects.all()
    return render(request, 'cart/order_admin.html', {'orders': orders})

@login_required
def update_order_status(request, order_id):


    if request.method == 'POST':
        new_status = request.POST.get('new_status')  
        order = Order.objects.get(id=order_id)  
        order.order_status = new_status 
        order.save()  
        return redirect('order_admin') 
    
@login_required
def order(request):
    user = request.user
    orders = Order.objects.filter(user=user)  
    return render(request, 'cart/order.html', {'orders': orders})




@login_required
def submit_review(request, order_item_id):
    if request.method == 'POST':
        review_text = request.POST.get('review')
        rating = request.POST.get('rating')
        if not review_text or not rating:
            messages.error(request, "Please fill in both review and rating fields.")
            return redirect('order')
        try:
            rating = int(rating) 
            if rating < 1 or rating > 5:
                messages.error(request, "Rating must be between 1 and 5.")
                return redirect('order')
        except ValueError:
            messages.error(request, "Invalid rating format.")
            return redirect('order')
        
        order_item = OrderItem.objects.get(id=order_item_id)  
        order_item.review = review_text  
        order_item.rating = rating  
        order_item.save()  
        return redirect('order')  
    else:
        pass  
def delete_order(request, order_id):
   
    order = get_object_or_404(Order, id=order_id)
    
   
    if request.method == 'POST':
        
        order.delete()
        
        return redirect('order_admin')
    else:
       
        return redirect('order_admin')