"""Defines URL patterns for Inventories app."""

from django.urls import path
from . import views
from django.conf.urls.static import static 
from django.conf import settings
app_name = 'inventories'

urlpatterns = [
    path('', views.index, name="index"), 
    path('reports/', views.reports, name="reports"),
    path('basket/', views.basket, name = "basket"),
  
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
