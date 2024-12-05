from django.contrib import admin
from .models import Bus

# Register your models here so can be used at the admin model
@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("BusId", "CarPlateNo", "Capacity", "IsActive")