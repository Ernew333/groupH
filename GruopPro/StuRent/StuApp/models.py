from django.db import models

# Create your models here 


class Equipment(models.Model):
    
    name = models.CharField(max_length=50)
    Status = models.CharField( max_length=50)
    quantity = models.IntegerField()
    deviceType = models.CharField( max_length=50)
    serialNumber = models.CharField( max_length=50)
    created = models.DateTimeField( auto_now_add=False)
    updated = models.DateTimeField( auto_now=False)
    CPU = models.CharField(max_length=50)
    GPU = models.CharField(max_length=50)
    RAM = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    comments = models.TextField(null = True, blank = True)
    
    def __str__(self):
        return self.name
    
    
    
class Bookings(models.Model):
    
    
    Date = models.DateTimeField( auto_now = False,auto_now_add=False)
    Status = models.CharField( max_length=50)
    euipId =  models.ForeignKey(Equipment,on_delete=models.SET_NULL, null = True)
   # add userId but premade from django resear
    
    def __str__(self):
        return self.Status
    
    
    

