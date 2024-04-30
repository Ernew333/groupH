"""Defines URL patterns for Inventories app."""

from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'inventories'

urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/', include('accounts.urls')),
    path('item/<int:item_id>/', views.item, name='item'),
    path('reports/', views.reports, name="reports"),
    path('basket/', views.basket, name = "basket"),
    path('confirmed/', views.bkconfirmed, name='confirmed'),
    path('booking/', views.viewBooking, name = "viewbooking"), # View booking URL pattern
    path('cancel_booking/<str:id>/', views.cancelBooking, name = "cancelbooking") # Cancel booking URL pattern    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
