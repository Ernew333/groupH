from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import Item, Booking
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from datetime import date # importing date
from .forms import ItemForm

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
    
    sort = getSort(request)
    if not isSortEmpty(sort):
        items = sortItemsBy(items, sort)
        
    page = getPage(request, items)

    context = {
        'types': types,
        'statuses': statuses,
        'selectedTypeFilters': filters.get('type'),
        'selectedStatusFilters': filters.get('status'),
        'totalItems': totalItems,
        'sort': sort,
        'page': page,
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

def getSelectedFilters(request):   
    filters = {}

    filters['type'] = request.GET.getlist('typeOption')
    filters['status'] = request.GET.getlist('statusOption')

    return filters

def isFiltersEmpty(filters):
    for filterList in filters.values():
        if filterList:
            return False

    return True

def applyFilter(items, filters):
    typeFilters = filters.get('type')
    statusFilters = filters.get('status')
    filteredItems = items

    if  typeFilters:
        filteredItems = filteredItems.filter(type__in=typeFilters)

    if statusFilters:
        filteredItems = filteredItems.filter(status__in=statusFilters)

    return filteredItems

def getSort(request):
    return request.GET.get('sort')

def isSortEmpty(sort):
    return sort == None

def sortItemsBy(items, sort):
    if sort == 'name':
        items = items.order_by('name')
    elif sort == 'auditOldest':
        items = items.order_by('audit')
    elif sort == 'auditNewest':
        items = items.order_by('-audit')

    return items

def getPage(request, items):
    paginator = Paginator(items, 20)
    requestedPageNumber = request.GET.get('page')
    return paginator.get_page(requestedPageNumber)

def item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    quantity_range = range(1, item.quantity + 1)  # Generating the range from 1 to item.quantity
    context = {'item': item, 'quantity_range': quantity_range}
    return render(request, 'inventories/item.html', context)

""" Author: w1939035-Ernesto Cosentino """
def basket(request):
    #get all bookings 
    bookings = Booking.objects.all()
    #if delete is triggered in the basket page witch is a button then get the pk of the booking 
    if request.method == 'POST':
        if 'delete' in request.POST:
            pk = request.POST.get('delete')
            #get the same id object from the database 
            booking = Booking.objects.get(id=pk)
            #delete it 
            booking.delete()
    #render the basket page
    return render(request, 'inventories/basket.html', {"bookings": bookings})
    
""" Author: w1939035-Ernesto Cosentino """
def reports(request):
    #render the reports page 
    return render(request, "inventories/reports.html")

def bkconfirmed(request):
    return render(request, 'inventories/bkconfirmed.html')

def viewBooking(request):
    completed_bookings = Booking.objects.filter(end_date__lt=date.today()) # Checks if booking is completed by checking if its past current date
    for cb in completed_bookings: # For loop iterates completed_bookings
        cb.status = "Completed" # Status changed to completed and saves it
        cb.save()
    booking = Booking.objects.all() # Retrieve all bookings from database
    return render(request, 'inventories/bookings.html',{'booking': booking }) # Booking page is rendered with all booking retrived from database

def cancelBooking(request,id):
    cancel_booking = Booking.objects.get(id=id) # Retrieves id of booking your trying to cancel
    cancel_booking.status = "Cancelled" # Changes the status to cancelled and saves it 
    cancel_booking.save()
    return redirect('inventories:viewbooking') # Redirects you back to view booking page

def manageItem(request):
    item = Item.objects.all() # Retrieves all items from the database
    context = {'item': item} # The items are passed onto the template  
    return render(request,'inventories/manageitem.html', context) # Render the manage item page items retrieved from the database

def createItem(request):
    form = ItemForm()

    if request.method == 'POST': # Checks if the method is post
        form = ItemForm(request.POST) # The form instance stores the data from the POST
        if form.is_valid():# Check if the form is valid and if it is the data will get saved to database
            form.save()
            return redirect('inventories:manageitem')# Redirects back to manage item page 
    context = {'form': form} # Form passed into the template 
    return render(request, 'inventories/item_form.html', context) # Renders the form page

def updateItem(request,id):
    item = Item.objects.get(id=id) # Retrieves item by its id
    form = ItemForm(instance=item) # Instance of the form is created stored the item data

    if request.method == 'POST': # Checks if the method is post
        form = ItemForm(request.POST, instance=item) # The form instance stores the data from the POST
        if form.is_valid(): # Check if the form is valid and if it is the data will get saved to database
            form.save()
            return redirect('inventories:manageitem')# Redirects back to manage item page 

    context = {'form': form}
    return render(request, 'inventories/item_form.html', context) # Renders the form page

def deleteItem(request, id):
    item = Item.objects.get(id=id) # Retrieves item by its id
    context = {'item': item} # The items are passed onto the template 
    if request.method == 'POST': # Checks if the method is post
        item.delete() # Item will be deleted
        return redirect('inventories:manageitem') # Redirects back to the manage item page 
    return render(request, 'inventories/delete.html', {'item': item }) # Renders the delete page which asks if you really want to delete. 
