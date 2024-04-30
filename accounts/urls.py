from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('', views.index, name="index"),#URL pattern for the index page
    path('manageuser/', views.manageuser, name = "manageuser"),#URL pattern for the manage user page
    path('deleteuser/<str:id>/', views.deleteuser, name = "deleteuser"),
    path('adduser', views.adduser, name = "adduser"),
]