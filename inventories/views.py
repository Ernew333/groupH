from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Item
from django.core.paginator import Paginator

# Create your views here.
@login_required
def index(request):
    items = Item.objects.all()
    totalItems = items.count()

    types = getTypes(items)
    statuses = getStatuses(items)

    page = getPageItems(request, items)

    context = {'page': page, 'types': types, 'statuses': statuses, 'totalItems': totalItems}
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

def getPageItems(request, items):
    paginator = Paginator(items, 1)
    requestedPageNumber = request.GET.get('page')
    itemsInPage = paginator.get_page(requestedPageNumber)

    return itemsInPage