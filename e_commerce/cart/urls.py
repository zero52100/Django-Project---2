from django.urls import path
from . import views

urlpatterns = [
    path('view_cart/', views.view_cart, name='view_cart'),
    path('cart/increment/<int:item_id>/', views.increment_item, name='increment_item'),
    path('cart/decrement/<int:item_id>/', views.decrement_item, name='decrement_item'),
    path('shipping_address/', views.shipping_address, name='shipping_address'),
    path('payment/', views.payment, name='payment'),
    path('checkout/', views.checkout, name='checkout'),
    path('process_order', views.process_order, name='process_order'),
    path('order/', views.order, name='order'),
    path('order_admin/', views.order_admin, name='order_admin'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('submit_review/<int:order_item_id>/', views.submit_review, name='submit_review'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    
    
   
    


    

    
    
    
    
]