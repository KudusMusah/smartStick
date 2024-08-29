from django.db import models

# Create your models here.
class Stick(models.Model):
    stick_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.stick_id    
    


class StickInfo(models.Model):
    stick = models.OneToOneField(Stick, on_delete=models.CASCADE, blank=True, null=True)
    owner_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact = models.CharField(max_length=12)
    starting_location = models.CharField(max_length=200)
    final_destinations = models.TextField()
    