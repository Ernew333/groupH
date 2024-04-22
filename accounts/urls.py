from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('createitem/', views.createItem, name = "start_createitem"),
    path('updateitem/<str:id>/', views.updateItem, name = "start_updateitem"),
    path('deleteitem/<str:id>/', views.deleteItem, name = "start_deleteitem"),
]