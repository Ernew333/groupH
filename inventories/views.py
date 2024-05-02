#Edwin domale 
# Azim Shahul Hameed
#Ernesto Cosentino
# Nayim Amdouni
# Muhammad Ozair Khan
from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import Item, Booking
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from datetime import date # importing date
from django.utils import timezone
from .forms import ItemForm

@login_required
def index(request):

    searchQuery = request.GET.get('query')

    items = Item.objects.all().order_by('name')


    if searchQuery:
        items = items.filter(Q(name__icontains=searchQuery))


    types = getTypes(items)
    statuses = getStatuses(items)

    filters = getSelectedFilters(request)

    if not isFiltersEmpty(filters):
        items = applyFilter(items, filters)

        itemsFilteredBySelectedType = Item.objects.filter(typein=filters.get('type'))
        itemsFilteredBySelectedStatus = Item.objects.filter(statusin=filters.get('status'))

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
@login_required
def basket(request,item_id):
    #get the items based on the id 
    item = Item.objects.get(id=item_id) 
    #render the basket page
    return render(request, 'inventories/basket.html', {"item": item})
    
""" Author: w1939035-Ernesto Cosentino """
@login_required
def reports(request):
    #render the reports page 
    return render(request, "inventories/reports.html")

""" Author: w1939035-Ernesto Cosentino """
@login_required
def bkconfirmed(request, item_id):
    
    user = request.user

    # Get the item or  404 error if not 
    item = get_object_or_404(Item, id=item_id)

    # Set booking dates, to the time the booking has been made 
    start_date = timezone.now()
    end_date = start_date + timezone.timedelta(days=10)  #all bookings whould be returned within 10 days max

    # Create the booking record
    booking = Booking.objects.create(
        item=item,
        user=user,
        start_date=start_date,
        end_date=end_date,
        status=Booking.BookingStatus.ACTIVE 
    )
    
    context =  {'bookingRef': booking.id}

    # Render a confirmation page and pass the booking reference
    return render(request, 'inventories/bkconfirmed.html', context)

@login_required
def viewBooking(request):
    user = request.user  # Retrieve the logged-in user
    if user.is_superuser:
        completed_bookings = Booking.objects.filter(end_date__lt=date.today(), user=request.user)# Checks if booking is completed by checking if its past current date
        booking = Booking.objects.all() # Retrieve all bookings from database
        return render(request, 'inventories/bookings.html',{'booking': booking }) # Booking page is rendered with all booking retrived from database
    else:
        completed_bookings = Booking.objects.filter(user=user, end_date__lt=date.today())  # Filter completed bookings by the logged-in user and end date
        booking = Booking.objects.filter(user=user)  # Filter bookings by the logged-in user
        return render(request, 'inventories/bookings.html',{'booking': booking }) 


def cancelBooking(request,id):
    cancel_booking = Booking.objects.get(id=id) # Retrieves id of booking your trying to cancel
    cancel_booking.status = "Cancelled" # Changes the status to cancelled and saves it 
    cancel_booking.save()
    return redirect('inventories:viewbooking') # Redirects you back to view booking page

@login_required
def manageItem(request):
    item = Item.objects.all() # Retrieves all items from the database
    context = {'item': item} # The items are passed onto the template  
    return render(request,'inventories/manageitem.html', context) # Render the manage item page items retrieved from the database

@login_required
def createItem(request):
    form = ItemForm()

    if request.method == 'POST': # Checks if the method is post
        form = ItemForm(request.POST, request.FILES) # The form instance stores the data from the POST
        if form.is_valid():# Check if the form is valid and if it is the data will get saved to database
            form.save()
            return redirect('inventories:manageitem')# Redirects back to manage item page 
    context = {'form': form} # Form passed into the template 
    return render(request, 'inventories/item_form.html', context) # Renders the form page

@login_required
def updateItem(request,id):
    item = Item.objects.get(id=id) # Retrieves item by its id
    form = ItemForm(instance=item) # Instance of the form is created stored the item data

    if request.method == 'POST': # Checks if the method is post
        form = ItemForm(request.POST, request.FILES, instance=item) # The form instance stores the data from the POST
        if form.is_valid(): # Check if the form is valid and if it is the data will get saved to database
            form.save()
            return redirect('inventories:manageitem')# Redirects back to manage item page 

    context = {'form': form}
    return render(request, 'inventories/item_form.html', context) # Renders the form page

@login_required
def deleteItem(request, id):
    item = Item.objects.get(id=id) # Retrieves item by its id
    context = {'item': item} # The items are passed onto the template 
    if request.method == 'POST': # Checks if the method is post
        item.delete() # Item will be deleted
        return redirect('inventories:manageitem') # Redirects back to the manage item page 
    return render(request, 'inventories/delete.html', {'item': item }) # Renders the delete page which asks if you really want to delete.

@login_required
def report_results(request):
    if request.method == 'POST':
        reportType = request.POST.get('reportType')
        context = {'reportType': reportType}
#if reportype is inventory show the current status of the inventory and incle name the type location and status 
        if reportType == 'inventory status':
            context['items'] = Item.objects.values('name', 'type', 'location', 'status')
            #shows the items that have been booked 
        elif reportType == 'equipment usage':
            context['bookings'] = Booking.objects.values('item__name', 'status')
            #shows the equipments that have been overdue 
        elif reportType == 'overdue equipment':
            overdue_date = timezone.now()
            context['bookings'] = Booking.objects.filter(end_date__lt=overdue_date, status=Booking.BookingStatus.ACTIVE).values('id', 'item__name', 'end_date')
        elif reportType == 'number of equipment':
            #showss the number of equipments 
            context['items'] = Item.objects.values('name','quantity')

        return render(request, "inventories/report_results.html", context)
    else:
        return render(request, "inventories/reports.html")

""" Author: w1939035-Ernesto Cosentino """
@login_required
def reports(request):
    return render(request, "inventories/reports.html")
