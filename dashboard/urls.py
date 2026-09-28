from django.contrib import admin
from django.urls import path
from .views import dashboard_data

urlpatterns = [
    path('', dashboard_data, name='dashboard'),
]