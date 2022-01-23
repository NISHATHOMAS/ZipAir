from django.db import models


class Config(models.Model):
    """Configurations as per requirement, all in Litters"""
    capacity_multiplier = models.IntegerField(default=200)
    consumption_multiplier = models.FloatField(default=.080)
    passenger_consumption_multiplier = models.FloatField(default=.002)


class AirLine(models.Model):
    """Definition of an Airline"""
    name = models.CharField(max_length=64)
    airline_id = models.IntegerField(db_index=True, unique=True)
    fuel_capacity = models.FloatField()
    passengers = models.IntegerField(default=1)
    airline_fuel_consumption = models.FloatField()
    passenger_fuel_consumption = models.FloatField()
    total_fuel_consumption = models.FloatField()
    maximum_travel_time = models.DurationField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
