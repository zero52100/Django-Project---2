from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),

    
     path('contact', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    # path('user_v/', views.user_v, name='user_v'),
    path('verify/', views.verify_otp, name='verify'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('set_password/', views.set_password, name='set_password'),
    path('password_reset_otp/', views.password_reset_otp, name='password_reset_otp'),
    path('logout/', views.logout_view, name='logout'),
     path('search_and_filter/', views.search_and_filter_products, name='search_and_filter')
    ]
    
    
    
    

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)