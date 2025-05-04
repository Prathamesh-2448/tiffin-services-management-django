from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('monthly', views.monthly, name='monthly'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add-customers/', views.add_customers, name='add-customers'),
]