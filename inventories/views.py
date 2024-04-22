from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Item
from .forms import ItemForm


# Create your views here.
@login_required
def index(request):
    return render(request, 'inventories/index.html')

def manageitem(request):
    item = Item.objects.all()
    context = {'item': item}
    return render(request,'inventories/manageitem.html', context)

def createItem(request):
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventories:manageitem')
    context = {'form': form}
    return render(request, 'inventories/item_form.html', context)

def updateItem(request,id):
    item = Item.objects.get(id=id)
    form = ItemForm(instance=item)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventories:manageitem')

    context = {'form': form}
    return render(request, 'inventories/item_form.html', context)

def deleteItem(request, id):
    item = Item.objects.get(id=id)
    context = {'item': item}
    if request.method == 'POST':
        item.delete()
        return redirect('inventories:manageitem')
    return render(request, 'inventories/delete.html', {'item': item })
