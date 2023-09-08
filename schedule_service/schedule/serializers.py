from rest_framework import serializers
from .models import *
import logging
logger=logging.getLogger(__name__)

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'airport_name', 'city','status']



class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'seating_capacity','status']

class ScheduleSerializer(serializers.ModelSerializer):
    source_airport = AirportSerializer()
    destination_airport = AirportSerializer()
    flight = FlightSerializer()

    class Meta:
        model = Schedule
        fields =  ['id', 'source_airport', 'destination_airport', 'flight','arrival_time','departure_time','base_price','status']

    def create(self, validated_data):
        logger.info("enter into create")
        source_airport_data = validated_data.pop('source_airport')
        try:
            source_airport = Airport.objects.filter(
                **source_airport_data).first()
            if source_airport is None:
                raise Airport.DoesNotExist
            if source_airport.status != 'Active':
                raise serializers.ValidationError("Airport is not active.")

        except Airport.DoesNotExist:
            raise serializers.ValidationError("Source airport does not exist.")

        destination_airport_data = validated_data.pop('destination_airport')
        try:
            destination_airport = Airport.objects.filter(
                **destination_airport_data).first()
            if destination_airport is None:
                raise Airport.DoesNotExist
            if destination_airport.status != 'Active':
                raise serializers.ValidationError("Airport is not active.")
        except Airport.DoesNotExist:
            raise serializers.ValidationError(
                "destination airport does not exist.")
        if(source_airport ==destination_airport ):
            raise serializers.ValidationError("Source Airport and Destination Airport are same")
        
        flight_data = validated_data.pop('flight')
        try:
            flight = Flight.objects.filter(**flight_data).first()
            if flight is None:
                raise Flight.DoesNotExist
            if flight.status != 'Active':
                raise serializers.ValidationError("Flight is not active.")
        except Flight.DoesNotExist:
            raise serializers.ValidationError("flight does not exist.")
        logger.info("enter ")
        seating_capacity = flight.seating_capacity
        validated_data['available_seats'] = seating_capacity
        
        try:
            logger.info("enter into try")
            schedule = Schedule.objects.create(
                source_airport=source_airport,
                destination_airport=destination_airport,
                flight=flight,
                **validated_data
            )
        except Exception:
            logger.info("exception occured")
            raise serializers.ValidationError("Failed to create schedule.")
        return schedule

      
class SchedulesSerializer(serializers.ModelSerializer):
    source_airport = AirportSerializer()
    destination_airport = AirportSerializer()
    flight = FlightSerializer()

    class Meta:
        model = Schedule
        fields = '__all__'

    def update(self, instance, validated_data):
        source_airport_data = validated_data.pop('source_airport')
        try:
            source_airport = Airport.objects.filter(
                **source_airport_data).first()

            if source_airport is None:
                raise Airport.DoesNotExist
        except Airport.DoesNotExist:
            raise serializers.ValidationError("Source airport does not exist.")

        destination_airport_data = validated_data.pop('destination_airport')
        try:
            destination_airport = Airport.objects.filter(**destination_airport_data).first()
            if destination_airport is None:
                raise Airport.DoesNotExist
        except Airport.DoesNotExist:
            raise serializers.ValidationError("Destination airport does not exist.")

        flight_data = validated_data.pop('flight')
        try:
            flight = Flight.objects.filter(**flight_data).first()
            if flight is None:
                raise Flight.DoesNotExist
        except Flight.DoesNotExist:
            raise serializers.ValidationError("Flight does not exist.")

        # Update the instance with the new data
        instance.source_airport = source_airport
        instance.destination_airport = destination_airport
        instance.flight = flight

        instance.arrival_time = validated_data.get('arrival_time', instance.arrival_time)  # Update other fields as needed
        instance.departure_time = validated_data.get('departure_time', instance.departure_time)
        instance.available_seats = validated_data.get('available_seats', instance.available_seats)
        instance.base_price = validated_data.get('base_price', instance.base_price)
       
        # ...

        instance.save()  # Save the updated instance
        return instance


class ScheduleRetrevieSerializer(serializers.ModelSerializer):
    source_airport = AirportSerializer()
    destination_airport = AirportSerializer()
    flight = FlightSerializer()

    class Meta:
        model = Schedule
        fields = '__all__'
