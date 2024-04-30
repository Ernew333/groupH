
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Item, Booking
from django.db.models import Count 


def index(request):
    return render(request, 'inventories/index.html')



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





def reports(request):
    return render(request, "inventories/reports.html")
