from django.db import models
from django.db.models import JSONField

class BookingData(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    booked_date = models.DateField()
    seats = JSONField() 
    

    def __str__(self):
        return f"{self.name} - {self.booked_date}"

