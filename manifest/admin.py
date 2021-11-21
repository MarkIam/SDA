from django.contrib import admin
from manifest.models import Skydiver

# Register your models here.
@admin.register(Skydiver)
class SdaAdmin(admin.ModelAdmin):
    list_filter = ('last_name', 'first_name')    
    list_filter = ('last_name', 'phone_number')