"""Defines URL patterns for Inventories app."""

from django.urls import path
from . import views

app_name = 'inventories'

urlpatterns = [#all URL patterns used
    path('', views.index, name="index"),#index page URL pattern
    path('booking/', views.viewBooking, name = "viewbooking"),# view booking URL pattern
    path('cancel_booking/<str:id>/', views.cancelBooking, name = "cancelbooking"),#cancel booking URL pattern
]