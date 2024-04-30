"""Defines URL patterns for Inventories app."""

from django.urls import path
from . import views

app_name = 'inventories'

urlpatterns = [
    path('', views.index, name="index"), 
    path('reports/', views.reports, name="reports"),
    path('report_results/', views.report_results, name="report_results")
]