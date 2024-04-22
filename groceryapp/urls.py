"""
URL configuration for grocery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from .middlewares.auth import  auth_middleware

urlpatterns = [
  path('', views.index, name='home'),
  path('product/<int:product_id>/', views.product_view, name='product_view'),
   path('about/', views.about, name='about'),
   path('signin/', views.sign, name='sign'),
   path('logout/', views.logout, name='logout'),
   path('cart/', views.carts, name='cart'),
   path('account/',auth_middleware( views.account), name='cart'),
    path('order/',auth_middleware( views.order), name='order'),
   ]
