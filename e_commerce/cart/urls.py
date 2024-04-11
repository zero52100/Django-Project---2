from django.urls import path
from . import views

urlpatterns = [
    path('view_cart/', views.view_cart, name='view_cart'),
    path('cart/increment/<int:item_id>/', views.increment_item, name='increment_item'),
    path('cart/decrement/<int:item_id>/', views.decrement_item, name='decrement_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    
    


    

    
    
    
    
]