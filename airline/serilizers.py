from datetime import timedelta

import math
from decimal import Decimal
from rest_framework import serializers

from airline.models import AirLine, Config


class CreateAirLineSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    airline_id = serializers.IntegerField(required=True)
    passengers = serializers.IntegerField(required=True)
    fuel_capacity = serializers.SerializerMethodField()
    airline_fuel_consumption = serializers.SerializerMethodField()
    passenger_fuel_consumption = serializers.SerializerMethodField()
    total_fuel_consumption = serializers.SerializerMethodField()
    maximum_travel_time = serializers.SerializerMethodField()

    def get_fuel_capacity(self, obj):
        self.fuel_capacity = Config.objects.first().capacity_multiplier*obj.airline_id
        return self.fuel_capacity

    def get_airline_fuel_consumption(self, obj):
        self.airline_fuel_consumption = round((Config.objects.first().consumption_multiplier * math.log(obj.airline_id, 10)), 3)
        return self.airline_fuel_consumption

    def get_passenger_fuel_consumption(self, obj):
        self.passenger_fuel_consumption = round((Config.objects.first().passenger_consumption_multiplier * obj.passengers), 3)
        return self.passenger_fuel_consumption

    def get_total_fuel_consumption(self, obj):
        self.total_fuel_consumption = round((self.get_airline_fuel_consumption(obj) + self.get_passenger_fuel_consumption(obj)), 3)
        return self.total_fuel_consumption

    def get_maximum_travel_time(self, obj):
        self.maximum_travel_time = timedelta(minutes=round((self.fuel_capacity/self.total_fuel_consumption), 3))
        return self.maximum_travel_time

    def create(self, validated_data):
        airline_obj = AirLine(**validated_data)
        validated_data["fuel_capacity"] = self.get_fuel_capacity(airline_obj)
        validated_data["passenger_fuel_consumption"] = self.get_passenger_fuel_consumption(airline_obj)
        validated_data["airline_fuel_consumption"] = self.get_airline_fuel_consumption(airline_obj)
        validated_data["total_fuel_consumption"] = self.get_total_fuel_consumption(airline_obj)
        validated_data["maximum_travel_time"] = self.get_maximum_travel_time(airline_obj)
        print("validated_data", validated_data["airline_id"], validated_data["total_fuel_consumption"])
        airline_obj = AirLine(**validated_data)
        print(airline_obj)
        airline_obj.save()
        return airline_obj

    def __init__(self, *args, **kwargs):
        super(CreateAirLineSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = AirLine
        fields = ("name",
                  "airline_id",
                  "passengers",
                  "fuel_capacity",
                  "airline_fuel_consumption",
                  "passenger_fuel_consumption",
                  "total_fuel_consumption",
                  "maximum_travel_time")
