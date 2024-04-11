from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import SignUpForm, ContactForm, LoginForm, ResetForm,SetPasswordForm
from .models import CustomUser
from products_app.models import Product 
from django.core.mail import send_mail
from decimal import Decimal
import random
from django.contrib import messages
def home(request):
    product_list=Product.objects.all()
    
   
    
    
    for product in product_list:
        # Calculate discounted price
        discounted_price = product.price - (product.price * product.discount_percentage / Decimal(100))
        # Update product object with discounted price
        product.discounted_price = discounted_price
    return render(request, 'users/home.html',{'product_list':product_list})
def search_and_filter_products(request):
    product_list = Product.objects.all()
    
    # Handle search functionality
    query = request.GET.get('q')
    if query:
        product_list = product_list.filter(
            Q(Product_name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand_name__icontains=query)
        )
    
    # Handle filter functionality
    category = request.GET.get('category')
    discount_percentage = request.GET.get('discount_percentage')
    available_quantity=request.GET.get('available_quantity')
    price=request.GET.get('price')

    
    if category:
        product_list = product_list.filter(category=category)
    if available_quantity:
        if available_quantity == 'in-stock':
            product_list = product_list.filter(available_quantity__gte=1)
        elif available_quantity == 'out-Of-stock':
            product_list = product_list.filter(available_quantity=0)
    if price:
        if price == 'in-stock':
            product_list = product_list.filter(price__gte=1)
        elif price == 'out-Of-stock':
            product_list = product_list.filter(available_quantity=0)
    if discount_percentage:
        if discount_percentage == '10ormore':
            product_list = product_list.filter(discount_percentage__gte=10) 
        elif discount_percentage == '35ormore':
            product_list = product_list.filter(discount_percentage__gte=35) 
        elif discount_percentage == '50ormore':
            product_list = product_list.filter(discount_percentage__gte=50)  
        elif discount_percentage == '60ormore':
            product_list = product_list.filter(discount_percentage__gte=60)
    sort_by = request.GET.get('sort_by')
    if sort_by:
        if sort_by == 'name_asc':
            product_list = product_list.order_by('Product_name')
        elif sort_by == 'name_desc':
            product_list = product_list.order_by('-Product_name')
        elif sort_by == 'price_asc':
            product_list = product_list.order_by('price')
        elif sort_by == 'price_desc':
            product_list = product_list.order_by('-price')
    for product in product_list:
        discounted_price = product.price - (product.price * product.discount_percentage / Decimal(100))
        product.discounted_price = discounted_price
    
    return render(request, 'users/home.html', {'product_list': product_list})
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = ContactMessage(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            contact_message.save()
            return redirect('home.html')  # Redirect to a success page
    else:
        form = ContactForm()
    return render(request, 'users/contact.html', {'form': form})

# Generate OTP
def generate_otp():
    return random.randint(100000, 999999)

# Send OTP via email
def send_otp_email(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP is: {otp}'
    send_mail(subject, message, None, [email])

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User is not active until OTP verification
            otp = generate_otp()
            user.set_password(form.cleaned_data['password'])
            user.save()
            send_otp_email(user.email, otp)
            request.session['otp'] = otp
            request.session['email'] = user.email
            messages.success(request,"OTP send sucessfully,Please check your email for OTP")

            return redirect('verify')
    else:
        form = SignUpForm()
        
    return render(request, 'users/signup.html', {'form': form})

def verify_otp(request):

    if request.method == 'POST':
        
        otp = request.POST.get('otp')
        if otp == str(request.session['otp']):
            user = CustomUser.objects.get(email=request.session['email'])
            user.is_active = True
            user.save()
            messages.success(request,"Signup successful. Please login using your registered email id and password.")
            return redirect('login')
        else:
            messages.error(request, "Please enter correct OTP.")
            return render(request, 'users/verify.html')
    return render(request, 'users/verify.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Login successful.")
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                otp = generate_otp()
                user.otp = otp
                user.save()
                send_otp_email(email, otp)
                request.session['email'] = email
                return redirect('password_reset_otp')
            except CustomUser.DoesNotExist:
                form.add_error('email', 'No user with this email address.')
    else:
        form = ResetForm()
    return render(request, 'users/reset_password.html', {'form': form})

def password_reset_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.session.get('email')
        if email:
            try:
                user = CustomUser.objects.get(email=email, otp=otp)
                return redirect('set_password')
            except CustomUser.DoesNotExist:
                return render(request, 'users/password_reset_otp.html', {'error': 'Invalid OTP. Please try again.'})
        else:
            return redirect('reset_password')
    return render(request, 'users/password_reset_otp.html')

def set_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            email = request.session.get('email')
            if email:
                try:
                    user = CustomUser.objects.get(email=email)
                    user.set_password(new_password)
                    user.save()
                    return redirect('login')
                except CustomUser.DoesNotExist:
                    pass  # Handle the case where the user doesn't exist
    else:
        form = SetPasswordForm()
    return render(request, 'users/set_password.html', {'form': form})
def logout_view(request):
    logout(request)
    
    return redirect('home')  