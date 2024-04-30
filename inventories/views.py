from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Booking




@login_required
def index(request):
    #rendre the main page
    return render(request, 'inventories/index.html')

def reports(request):
    #render the reports page 
    return render(request, "inventories/reports.html")

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
    
    
