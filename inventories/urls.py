"""Defines URL patterns for Inventories app."""

from django.urls import path
from . import views

app_name = 'inventories'

urlpatterns = [#all of the URL Patterns for the project
    path('', views.index, name="index"),#URL pattern for the index page
    path('manageitem/', views.manageItem, name = "manageitem"),#URL pattern for the manage item page
    path('createitem/', views.createItem, name = "createitem"),#URL pattern for the create item page
    path('updateitem/<str:id>/', views.updateItem, name = "updateitem"),#URL pattern for the update item page
    path('deleteitem/<str:id>/', views.deleteItem, name = "deleteitem"),#URL pattern for the delete item page
]