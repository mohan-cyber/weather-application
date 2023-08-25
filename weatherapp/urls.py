from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.signup_view, name='signup'),
    path('login/', views.user_login, name='login'),
    path('search/', views.search, name='search'),
]