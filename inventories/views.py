from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Booking




@login_required
def index(request):
    return render(request, 'inventories/index.html')

def reports(request):
    return render(request, "inventories/reports.html")

def basket(request):
    bookings = Booking.objects.all()
    if request.method == 'POST':
        if 'delete' in request.POST:
            pk = request.POST.get('delete')
            booking = Booking.objects.get(id=pk)
            booking.delete()

    return render(request, 'inventories/basket.html', {"bookings": bookings})
    
    
