"""Defines URL patterns for Inventories app."""

from django.urls import path
from . import views

app_name = 'inventories'

urlpatterns = [
    path('', views.index, name="index"),
    path('booking/', views.viewBooking, name = "viewbooking"),
    path('cancel_booking/<str:id>/', views.cancelBooking, name = "cancelbooking"),
]