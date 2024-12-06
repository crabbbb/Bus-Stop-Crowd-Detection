from django.contrib import admin
from .models import Bus, Schedule, Assignment, BusStation, BusTrackingLog, Route, RouteStation, ScheduleAssignment

# Register your models here so can be used at the admin model
# make register so the superuser can saw 
@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("BusId", "CarPlateNo", "Capacity", "IsActive")

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("ScheduleId", "IsActive", "CreateAt")

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("AssignmentId", "Time", "DayOfWeek", "BusId", "RouteId")

@admin.register(BusStation)
class BusStationAdmin(admin.ModelAdmin):
    list_display = ("StationId", "StationName", "IsActive")

@admin.register(BusTrackingLog)
class BusTrackingLogAdmin(admin.ModelAdmin):
    list_display = ("ArrivalDateTime", "AssignmentId", "BusStatus", "BusCapacityEstimate")

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("RouteId", "RouteDescription", "RouteDuration", "FromCampus", "IsActive")

@admin.register(RouteStation)
class RouteStationAdmin(admin.ModelAdmin):
    list_display = ("StationId", "RouteId", "RouteOrder")

@admin.register(ScheduleAssignment)
class ScheduleAssignmentAdmin(admin.ModelAdmin):
    list_display = ("ScheduleId", "AssignmentId")