from django.urls import path
# from .views import forgetpassword
from . import views 
from .views import *

urlpatterns = [
    
    # USER
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('bookup/', views.bookup, name='bookup'),
    path('book_vaccination/', BookingCreateView.as_view(), name='book_vaccination'),
     path('success', views.success, name='success'),
    # path('about/', views.about, name='about'),
    path('history', views.history, name='history'),
    path('forgetpassword', views.forgetpassword, name='forgetpassword'),
    
    
    
    # ADMIN
    path('login/', views.admin_login, name='login'),
    
]
 
 
    

