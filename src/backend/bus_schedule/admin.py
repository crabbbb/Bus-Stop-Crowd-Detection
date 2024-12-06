from django.contrib import admin
from .models import Bus, BusSchedule, BusScheduleAssignment, BusStation, BusTrackingLog, Route, RouteStation

# Register your models here so can be used at the admin model
# make register so the superuser can saw 
@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("BusId", "CarPlateNo", "Capacity", "IsActive")

@admin.register(BusSchedule)
class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ("ScheduleId", "DepartureTime", "ArrivalTime", "DayOfWeek")

@admin.register(BusScheduleAssignment)
class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ("AssignmentId", "ScheduleId", "RouteId", "BusId")

@admin.register(BusStation)
class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ("StationId", "StationName", "StationLocation", "IsActive")

@admin.register(BusTrackingLog)
class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ("ArrivalDateTime", "AssignmentId", "BusStatus", "BusCapacityEstimate")

@admin.register(Route)
class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ("RouteId", "RouteDescription", "IsActive", "FromCampus")

@admin.register(RouteStation)
class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ("StationId", "RouteId", "RouteDuration", "RouteOrder")