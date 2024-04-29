from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Item
from .forms import ItemForm


# Create your views here.
@login_required
def index(request):
    return render(request, 'inventories/index.html')#renders the index page

def manageItem(request):
    item = Item.objects.all()#retrieves all items from the database
    context = {'item': item}#the items are passed onto the template  
    return render(request,'inventories/manageitem.html', context)#render the manage item page items retrieved from the database

def createItem(request):
    form = ItemForm()

    if request.method == 'POST':#checks if the method is post
        form = ItemForm(request.POST)#the form instance stores the data from the POST
        if form.is_valid():#check if the form is valid and if it is the data will get saved to database
            form.save()
            return redirect('inventories:manageitem')# redirects back to manage item page 
    context = {'form': form}#form passed into the template 
    return render(request, 'inventories/item_form.html', context)#renders the form page

def updateItem(request,id):
    item = Item.objects.get(id=id)#retrieves item by its id
    form = ItemForm(instance=item)#instance of the form is created stored the item data

    if request.method == 'POST':#checks if the method is post
        form = ItemForm(request.POST, instance=item)#the form instance stores the data from the POST
        if form.is_valid():#check if the form is valid and if it is the data will get saved to database
            form.save()
            return redirect('inventories:manageitem')# redirects back to manage item page 

    context = {'form': form}
    return render(request, 'inventories/item_form.html', context)#renders the form page

def deleteItem(request, id):
    item = Item.objects.get(id=id)#retrieves item by its id
    context = {'item': item}#the items are passed onto the template 
    if request.method == 'POST':#checks if the method is post
        item.delete()#item will be deleted
        return redirect('inventories:manageitem')# redirects back to the manage item page 
    return render(request, 'inventories/delete.html', {'item': item })#renders the delete page which asks if you really want to delete. 
