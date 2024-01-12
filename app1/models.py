from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import datetime
# Create your models here.
class PostModel(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    passenger_name = models.CharField(max_length=255)  # Changed field name to snake_case
    date_of_journey = models.DateField()
    gender = models.CharField(max_length=1)
    flight_number = models.CharField(max_length=20)  # Changed to CharField assuming it can contain non-numeric characters
    pnr_number = models.CharField(max_length=20)  # Changed to CharField assuming it can contain non-numeric characters
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    baggage_space = models.IntegerField()  # Changed field name to snake_case
    is_checked = models.BooleanField(default=False)


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

#filter
# from django.db import models
#from django.contrib.auth.models import User

# class FilterModel(models.Model):
#     passenger_name = models.CharField(max_length=255)
#     date_of_journey = models.DateField()
#     gender = models.CharField(max_length=10)
#     flight_number = models.CharField(max_length=20)
#     pnr_number = models.CharField(max_length=20)
#     source = models.CharField(max_length=255)
#     destination = models.CharField(max_length=255)
#     baggage_space = models.CharField(max_length=10)
#     is_checked = models.BooleanField(default=False)
    
#     # New field for filtering (example: category)
#     category = models.CharField(max_length=255)

#     def __str__(self):
#         return f"{self.passenger_name} - {self.date_of_journey} - {self.destination}"
    

#rating
#from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Add any additional fields you might need for the user profile
class UserRating(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user_ratings')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user_ratings')
    rating = models.FloatField()  # You can customize this based on your rating system

    def __str__(self):
        return f"{self.from_user.username} rated {self.to_user.username} - {self.rating} stars"
