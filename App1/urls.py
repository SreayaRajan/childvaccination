from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('bookup/', views.bookup, name='bookup'),
    path('about/', views.about, name='about'),
    path('history', views.history, name='history'),
 
    
]
