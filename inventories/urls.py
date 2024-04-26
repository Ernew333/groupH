"""Defines URL patterns for Inventories app."""

from django.urls import path
from . import views

app_name = 'inventories'

urlpatterns = [
    path('', views.index, name="index"),
    path('manageitem/', views.manageItem, name = "manageitem"),
    path('createitem/', views.createItem, name = "createitem"),
    path('updateitem/<str:id>/', views.updateItem, name = "updateitem"),
    path('deleteitem/<str:id>/', views.deleteItem, name = "deleteitem"),
]