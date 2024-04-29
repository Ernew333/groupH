from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import Item , Booking#importing models needed for page 
from datetime import date#importing date


# Create your views here.
@login_required
def index(request):
    return render(request, 'inventories/index.html')#renders the index page

def viewBooking(request):
    completed_bookings = Booking.objects.filter(end_date__lt=date.today())#checks if booking is completed by checking if its past current date
    for cb in completed_bookings:#for loop iterates completed_bookings
        cb.status = "Completed"#status changed to completed and saves it
        cb.save()
    booking = Booking.objects.all()#retrieve all bookings from database
    return render(request, 'inventories/bookings.html',{'booking': booking })#booking page is rendered with all booking retrived from database

def cancelBooking(request,id):
    cancel_booking = Booking.objects.get(id=id)#retrieves id of booking your trying to cancel
    cancel_booking.status = "Cancelled"#changes the status to cancelled and saves it 
    cancel_booking.save()
    return redirect('inventories:viewbooking')#redirects you back to view booking page
    