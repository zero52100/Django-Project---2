from django.urls import path
from . import views

urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('view_product/', views.view_product, name='view_product'),
    
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
     path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    

    
    
    
    
]