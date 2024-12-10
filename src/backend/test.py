from backend.bus_schedule.models.Bus import Bus

bus1 = Bus(CarPlateNo="ABC123", Capacity=100, IsActive=True)
bus1.save()
print(bus1.id) 