from django.contrib import admin
from app1.models import PostModel
# Register your models here.



class PostModelAdmin(admin.ModelAdmin):
    list_display = ('passenger_name', 'date_of_journey', 'gender', 'flight_number', 'pnr_number', 'source', 'destination', 'baggage_space', 'is_checked')
    
admin.site.register(PostModel,PostModelAdmin)