from django.db import models

# Create your models here.
class SearchHistory(models.Model):
    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    search_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.origin} to {self.destination} on {self.departure_date}"
        
class Airport(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.code} - {self.name} ({self.city}, {self.country})"
