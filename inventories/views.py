from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Item

# Create your views here.
@login_required
def index(request):
    items = Item.objects.all()

    types = getTypes(items)
    statuses = getStatuses(items)

    context = {'items': items, 'types': types, 'statuses': statuses}
    return render(request, 'inventories/index.html', context)

def getTypes(items):
    types = {}

    for item in items:
        types[item.type] = countType(items, item.type)

    return types

def getStatuses(items):
    statuses = {}

    for item in items:
        statuses[item.status] = countStatus(items, item.status)

    return statuses

def countType(items, selectedType):
    return items.filter(type=selectedType).count()

def countStatus(items, selectedStatus):
    return items.filter(status=selectedStatus).count()