from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from django.contrib import messages
from .forms import CheckoutForm
from django.db import IntegrityError
from users.models import CustomUser
import stripe
from django.conf import settings
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
def checkout(request):
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
    return render(request, 'cart/checkout.html', {'form': form})


def payment(request):
    if request.method == 'POST':
        # Token is created using Checkout or Elements
        # Get the payment token ID submitted by the form:
        token = request.POST.get('stripeToken')

        try:
            # Charge the user's card:
            charge = stripe.Charge.create(
                amount=1000,  # Amount in cents
                currency='usd',
                description='Example charge',
                source=token,
            )
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(request, f"{err.get('message')}")
            return redirect('payment')  # Or render a payment error page
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(request, "Rate limit error")
            return redirect('payment')  # Or render a payment error page
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(request, "Invalid parameters")
            return redirect('payment')  # Or render a payment error page
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(request, "Authentication error")
            return redirect('payment')  # Or render a payment error page
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(request, "Network error")
            return redirect('payment')  # Or render a payment error page
        except stripe.error.StripeError as e:
            # Display a very generic error to the user
            messages.error(request, "Stripe error")
            return redirect('payment')  # Or render a payment error page
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(request, "Unknown error")
            return redirect('payment')  # Or render a payment error page

        # Payment successful
        return redirect('payment_success')  # Or render a payment success page

    return render(request, 'cart/payment.html')
