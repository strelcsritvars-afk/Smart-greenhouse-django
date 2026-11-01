from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard_data, name='dashboard'),
    path('plants/', plants_main, name='plants'),
    path('plants/add/', plant_add, name='plant_add'),
    path('plants/<int:pk>/edit/', plant_edit, name='plant_edit'),
    path('plants/<int:pk>/delete/', plant_delete, name='plant_delete'),
    path('plants/<int:pk>/assign_device/', plant_assign_device, name='plant_assign_device'),
    path("controllers/", controllers_main, name="controllers"),
    path("controllers/add/", controller_add, name="controller_add"),
    path("controllers/<int:pk>/edit/", controller_edit, name="controller_edit"),
    path("controllers/<int:pk>/delete/", controller_delete, name="controller_delete"),
    path("controllers/<int:pk>/plants/add/", controller_add_plant, name="controller_add_plant"),
]