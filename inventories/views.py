from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Item
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404


# Create your views here.
@login_required
def index(request):
    items = Item.objects.all().order_by('name')

    types = getTypes(items)
    statuses = getStatuses(items)
    
    filters = getSelectedFilters(request)

    if not isFiltersEmpty(filters):
        items = applyFilter(items, filters)
        
        itemsFilteredBySelectedType = Item.objects.filter(type__in=filters.get('type'))
        itemsFilteredBySelectedStatus = Item.objects.filter(status__in=filters.get('status'))

        if itemsFilteredBySelectedStatus:
            types = getTypes(itemsFilteredBySelectedStatus)

        if itemsFilteredBySelectedType:
            statuses = getStatuses(itemsFilteredBySelectedType)

    totalItems = items.count()
    page = getPage(request, items)

    context = {
        'types': types,
        'statuses': statuses,
        'selectedTypeFilters': filters.get('type'),
        'selectedStatusFilters': filters.get('status'),
        'totalItems': totalItems,
        'page': page
    }

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

def applyFilter(items, filters):
    typeFilters = filters.get('type')
    statusFilters = filters.get('status')
    filteredItems = items

    if  typeFilters:
        filteredItems = filteredItems.filter(type__in=typeFilters)

    if statusFilters:
        filteredItems = filteredItems.filter(status__in=statusFilters)

    return filteredItems

def isFiltersEmpty(filters):
    for filterList in filters.values():
        if filterList:
            return False

    return True

def getSelectedFilters(request):   
    filters = {}

    filters['type'] = request.GET.getlist('typeOption')
    filters['status'] = request.GET.getlist('statusOption')

    return filters

def getPage(request, items):
    paginator = Paginator(items, 1)
    requestedPageNumber = request.GET.get('page')
    return paginator.get_page(requestedPageNumber)

def item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    quantity_range = range(1, item.quantity + 1)  # Generating the range from 1 to item.quantity
    context = {'item': item, 'quantity_range': quantity_range}
    return render(request, 'inventories/item.html', context)
