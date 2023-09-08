from rest_framework import serializers
from booking.models import Seats
from rest_framework import serializers
from .models import Passenger, Transaction, Booking ,BookingHistory
from datetime import date as today_data
from django.db import connection, transaction, IntegrityError
from .custom_exceptions.DuplicatePNRNumber import DuplicatePNRNumberError

import logging

logger = logging.getLogger(__name__)

#BookingHistory 
class BookingHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingHistory
        fields = '__all__'

#seats 

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seats
        fields = ['scheduleId', 'seatNumber', 'isAvailable']

class TransactionSerializer(serializers.ModelSerializer):
    booking = serializers.PrimaryKeyRelatedField(source='booking.bookingId', read_only=True)

    class Meta:
        model = Transaction
        fields = ['transactionId', 'transactionStatus','transactionType','amount', 'booking']


class PassengerSerializer(serializers.ModelSerializer):
    booking = serializers.PrimaryKeyRelatedField(source='booking.bookingId', read_only=True)

    class Meta:
        model = Passenger
        fields = ['passengerId', 'passengerName', 'passengerAge', 'passengerAadhar', 'passengerStatus', 'seatNumber', 'booking']

class BookingRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    passengers = PassengerSerializer(many=True)
    


    class Meta:
        model = Booking
        fields = '__all__'
        
    
    def create(self, validated_data):
        transaction_data = validated_data.pop('transaction')
        passenger_data = validated_data.pop('passengers')

        # print(transaction_data)
 
        print(validated_data,"-----------------------------------")

        # Create the booking object with the transaction
        try:
            booking = Booking.objects.create( **validated_data)
        except :
            # logger.error()
            raise DuplicatePNRNumberError("Duplicate PNR Numer Submitted.........")
       
        print("created booking--------------------")

        # Create the transaction object
        transaction = Transaction.objects.create(booking=booking, **transaction_data)
        print("-----------------------ceated transaction")

        # Create the passenger objects and associate them with the booking
        for passenger_item in passenger_data:

            Passenger.objects.create(booking=booking, **passenger_item)
        print("created passengers ------------------------------------")

        return booking



