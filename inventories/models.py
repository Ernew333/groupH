#Edwin domale 
# Azim Shahul Hameed
#Ernesto Cosentino
# Nayim Amdouni
# Muhammad Ozair Khan
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Item(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    device_serial = models.CharField(max_length=50, blank=True)
    CPU = models.CharField(max_length=50, blank=True)
    GPU = models.CharField(max_length=10, blank=True)
    RAM = models.CharField(max_length=5, blank=True)    
    quantity = models.IntegerField()
    audit = models.DateField(null=True, blank=False)
    location = models.CharField(max_length=50)
    
    class ItemStatus(models.TextChoices):
        AVAILABLE = "Available", "Available"
        DECOMMISIONED = "Decommisioned", "Decommisioned"
        ON_LOAN = "On Loan", "On Loan"
        REPAIRING = "Repairing", "Repairing"

    status = models.CharField(max_length=13, choices=ItemStatus.choices, default=ItemStatus.AVAILABLE) 

    image = models.ImageField(upload_to='inventories/media/images')
    comments = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)

    class BookingStatus(models.TextChoices):
        ACTIVE = "Active", "Active"
        CANCELLED = "Cancelled", "Cancelled"
        COMPLETED = "Completed", "Completed"
        RESERVED = "Reserved", "Reserved"

    status = models.CharField(max_length=9, choices=BookingStatus.choices, default=BookingStatus.ACTIVE)

    def __str__(self):
        return "Ref. {}".format(str(self.id))
