from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Item , Booking
from datetime import date


# Create your views here.
@login_required
def index(request):
    return render(request, 'inventories/index.html')

def viewBooking(request):
    completed_bookings = Booking.objects.filter(end_date__lt=date.today())
    for cb in completed_bookings:
        cb.status = "Completed"
        cb.save()
    booking = Booking.objects.all()
    return render(request, 'inventories/bookings.html',{'booking': booking })