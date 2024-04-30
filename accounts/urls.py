from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.EditAccountView.as_view(), name='edit_account'),
    path('manageuser/', views.manageuser, name = "manageuser"), # URL pattern for the management of users
    path('deleteuser/<str:id>/', views.deleteuser, name = "deleteuser"), # URL pattern for the deletion of users
    path('adduser', views.adduser, name = "adduser"), # URL pattern for the addition of users    
]
