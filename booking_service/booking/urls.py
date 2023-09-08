
from django.urls import path
from booking.views import *


urlpatterns = [
    #seats
    path('rest/', seatSave),
    path('rest/<int:sid>/', seatUpdate, name='seat-update'),

    #booking
    path('booking/',booking ,name='booking'),
    path('getBooking/<int:id>',getBooking ,name='bookingId'),

    path('getTransactions/',TransactionInsertandGettingall.as_view() ,name='getTransactions'),
    path('transactionById/<int:pk>',TransactionUpadateAndDeleteAndRetraiveByID.as_view() ,name='transactionById'),
    
    path('getPassengers/',PassengerInsertandGettingall.as_view() ,name='getPassengers'),
    path('passengersById/<int:pk>',PassengerUpadateAndDeleteAndRetraiveByID.as_view() ,name='passengerById'),

    path('getTranactionByBookingId/<int:bookingId>',getTransactionByBookingId, name='getTransactionByBookingId' ),
    path('getPassengerByBookingId/<int:bookingId>', getPassengerByBookingId, name='getPassengerByBookingId' ),

    #Booking History
    path('bookingInsertandGettingall/',BookingInsertandGettingall.as_view(),name="BookingInsertandGettingall"),
    path('bookingupadateAndDeleteAndRetraiveByID/<int:pk>/',BookingUpadateAndDeleteAndRetraiveByID.as_view(),name="BookingUpadateAndDeleteAndRetraiveByID"),


]