
from django.contrib import admin
from django.urls import path,include
from . import views
from .middlewares.auth import  auth_middleware

urlpatterns = [
  path('', views.index, name='home'),
  path('product/<int:product_id>/', views.product_view, name='product_view'),
   path('about/', views.about, name='about'),
   path('contact/', auth_middleware(views.contact), name='about'),
   
   path('loginc/', views.loginc, name='loginc'),
   path('reset/', views.resetpassword, name='reset'),
   path('signup/', views.signup, name='signup'),
   path('logout/', views.logout, name='logoutc'),
   path('cart/', views.carts, name='cart'),
   path('account/',auth_middleware( views.account), name='cart'),
    path('order/',auth_middleware( views.order), name='order'),
     path('search/', views.product_search, name='product_search'),
     path('login/', views.user_login, name='login'),
     path('dashboard/', views.dashboard, name='dashboard'),
     path('pastorder/', views.pastorderdashboard, name='pastorder'),
  path('logout-admin/', views.logout_view,name='logout'),
  path('payment/', views.payment, name='logout'),
  path('prepaidorder/', views.onlinepayment, name='prepaid'),
  path('coddorder/', views.codorder, name='cod'),
  path('dsearch/', views.dashboard_search, name='dashboard_search'),
  path('privacy/', views.privacy, name='privacy'),
  path('terms&condition/', views.terms, name='terms&condition'),

   ]
