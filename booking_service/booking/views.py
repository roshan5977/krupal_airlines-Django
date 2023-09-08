from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from booking.serializer import *
from booking.models import *

#BookingHistory
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import  ListModelMixin,RetrieveModelMixin,DestroyModelMixin,CreateModelMixin,UpdateModelMixin
from django.shortcuts import render

from .serializer import BookingHistorySerializer
from .service import *

from django.db import transaction as trance, IntegrityError
import requests as reqs

import logging

logger = logging.getLogger(__name__)

@api_view(['POST', 'GET'])
def seatSave(request):

     if request.method == 'POST':
          logger.info("Schedule service POST method")
     
          serializer = SeatSerializer(data=request.data)
          if serializer.is_valid():
          
               serializer.save()
               s= Response(serializer.data, status=status.HTTP_201_CREATED)
               logger.info("{}".format(s.data))
               return s
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     else:
          logger.info("Schedule service GET method")
          seats = Seats.objects.all()
          serializer = SeatSerializer(seats, many=True)
          return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def seatUpdate(request, sid):

     seat = get_object_or_404(Seats, seatId=sid)

     if request.method == 'GET':
          logger.info("Schedule service by id  GET method")
          serializer = SeatSerializer(instance=seat)
          data=Response(serializer.data)
          logger.info(" {}".format(data.data))
          return data

               
     elif request.method == 'PUT' or request.method == 'PATCH':
          logger.info("Schedule service by id  PUT OR PATCH method")
          serializer = SeatSerializer(seat, data=request.data, partial=True)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     elif request.method == 'DELETE':
          logger.info("Schedule service by id  DELETE method")
          seat.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)
     
# -------------------------------------Transaction Operations--------------------------------------

class TransactionInsertandGettingall(GenericAPIView,CreateModelMixin,ListModelMixin):
     queryset = Transaction.objects.all()
     serializer_class=TransactionSerializer
     def post(self,request):
          logger.info("Transaction service POST method")
          trasaction =self.create(request)
         
          logger.info("---{}".format(trasaction.data))
          return trasaction
     def get(self,request):
          logger.info("Transaction service GET method")
          return self.list(request)

class TransactionUpadateAndDeleteAndRetraiveByID(GenericAPIView,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin):
     queryset=Transaction.objects.all()
     serializer_class=TransactionSerializer
     def put(self,request,**kwargs):
          logger.info("Transaction service By Id PUT method")
          return self.update(request,**kwargs)
     def delete(self,request,**kwargs):
          logger.info("Transaction service By Id DELETE method")
          return self.destroy(request,**kwargs)
     def get(self,request,**kwargs):
          logger.info("Transaction service BU Id GET method")
          return self.retrieve(request,**kwargs)
     
@api_view(['GET'])
def getTransactionByBookingId(request, bookingId):
     logger.info("Transaction service By Id GET method")
     transaction = Transaction.objects.filter(booking=bookingId)
     transactionSerializer = TransactionSerializer(instance = transaction)
     return Response(transactionSerializer.data, status=status.HTTP_200_OK)
     
# -------------------------------------Passengers Operations--------------------------------------

class PassengerInsertandGettingall(GenericAPIView,CreateModelMixin,ListModelMixin):
     queryset = Passenger.objects.all()
     serializer_class=PassengerSerializer
     def post(self,request):
          logger.info("Passengers service POST method")
          passengers = self.create(request)
          logger.info("---{}".format(passengers.data))
          return passengers
     def get(self,request):
          logger.info("Passengers service GET method")
          return self.list(request)
     
class PassengerUpadateAndDeleteAndRetraiveByID(GenericAPIView,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin):
     queryset=Passenger.objects.all()
     serializer_class=PassengerSerializer
     def put(self,request,**kwargs):
          logger.info("Passengers service By Id  PUT method")
          return self.update(request,**kwargs)
     def delete(self,request,**kwargs):
          logger.info("Passengers service By Id DELETE method")
          return self.destroy(request,**kwargs)
     def get(self,request,**kwargs):
          logger.info("Passengers service By Id GET method")
          return self.retrieve(request,**kwargs)
     
@api_view(['GET'])
def getPassengerByBookingId(request, bookingId):
     logger.info("Passengers service getPassengerByBookingId  GET method")
     passengers = Passenger.objects.filter(booking=bookingId)
     passengerSerializer = PassengerSerializer(data = passengers, many=True)
     passengerSerializer.is_valid()
     return Response(passengerSerializer.data, status=status.HTTP_200_OK)
# -------------------------------------Booking Operations--------------------------------------

@api_view(['POST','GET'])
def booking(request):
     if request.method == 'POST':
          try:
               with trance.atomic():
                    serializer = BookingSerializer(data = request.data)
                    if serializer.is_valid():
               
                         serializer.save()
                         booking = serializer.instance
                         booking_id = serializer.instance.bookingId

                         bookings = Booking.objects.get(bookingId = booking_id)
                         retriveSerializer = BookingRetrieveSerializer(instance = bookings)

                         transaction = Transaction.objects.get(booking = booking_id)
                         transactionSerializer = TransactionSerializer(instance = transaction)

                         passengers = Passenger.objects.filter(booking=booking_id)
                         passengerSerializer = PassengerSerializer(data = passengers, many=True)
                         passengerSerializer.is_valid()
                         
               
                       
                         # logger.info("****************************************************")
                         # # FOR GETTING NO OF TICKETS BOOKED PREVIOUSLI
                         # cursor = connection.cursor()
                         # cursor.execute(f"select sum(no_of_tickets_booked) from `booking-module`.booking_history where schedule_id={booking.scheduleId};")
                         # result = cursor.fetchone()
                         # logger.info(result[0]) #2 
                         # # tickets_booked_previous = int(result[0])
                         
                         # sum_of_tickets = 0

                         # if result[0] is None:
                         #      sum_of_tickets=0
                         # elif type(int(result[0])) == int:
                         #      sum_of_tickets = result[0]

                         
                         # logger.info("+++++++++++++++++++++++++{}".format(sum_of_tickets))
                         logger.info((booking.journeyDate - booking.bookingDate).days)

                         #getting schedule object for getiing flight seating capacity 
                         response = reqs.get(f"http://localhost:9003/schedule/getById/{booking.scheduleId}")
                         schedule_data = response.json()

                         avilable_seats_inschedule = schedule_data['flight']['seating_capacity'] - schedule_data['available_seats']

                         
                         # print("999999999999999999999999999999999999 {}".format(schedule_data['flight']['seating_capacity'])) 
                         seating_capacity = schedule_data['flight']['seating_capacity']
                         bookinghistory = BookingHistory(
                              available_tickets =seating_capacity-avilable_seats_inschedule -len(passengers),
                              date = booking.bookingDate,
                              days_left= (booking.journeyDate - booking.bookingDate).days,
                              no_of_tickets_booked = len(passengers),
                              schedule_id=booking.scheduleId
                              )
                         bh = BookingHistoryService()
                         bh.saveBh(bookinghistory)


                         logger.info(" {}".format(schedule_data))
                        
                         # updating seats avialable in schedule       
                         available_seats = int(seating_capacity-avilable_seats_inschedule-len(passengers))
                            
                         url = "http://localhost:9003/schedule/patchAvailableTickets/{}/{}/".format(schedule_data['id'],available_seats)   

                         
                         
                         
                         response = reqs.patch(url)
                         logger.info(response)

                         # bk = BookingHistory.objects.get(date=today_data.today())
                         # print(bk)

                         return Response([retriveSerializer.data,transactionSerializer.data,passengerSerializer.data], status= status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          except IntegrityError as i:
                    logger.info(i)
               
              
          
     else:
          booking = Booking.objects.all()
          serializer = BookingRetrieveSerializer(data=booking, many=True)
          serializer.is_valid()
          logger.info(serializer.data)
          return Response(serializer.data, status=status.HTTP_200_OK)
          

@api_view(['PUT','GET','DELETE'])
def getBooking(request,id):
     if request.method =='PUT':
          booking = Booking.objects.get(bookingId=id)
          serializer = BookingRetrieveSerializer(booking, data=request.data)
          if serializer.is_valid():
               serializer.save()

               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     elif request.method =='GET':
          booking = Booking.objects.get(bookingId=id)
          serializer = BookingRetrieveSerializer(instance = booking)
          return Response(serializer.data, status=status.HTTP_200_OK)
     else:
          booking = Booking.objects.get(bookingId=id)

          logger.info(" ++ {} {} {} {} {} {} {}" .format(booking.bookingDate,booking.bookingId,booking.email, 
                                                  booking.pnrNumber, booking.status, booking.journeyDate, booking.scheduleId))

          
          transaction = Transaction.objects.get(booking = id)
          
          passengers = Passenger.objects.filter(booking= id)

          logger.info(len(passengers))

          bh = BookingHistoryService()
          bh.deleteBh(booking.scheduleId, len(passengers),booking.bookingDate)

          # #rest call to update seats avilable in schedule modulle
          # url = "http://localhost:9003/schedule/patchAvailableTickets/{}/{}/".format(schedule_data['id'],available_seats)   
   
          # response = reqs.patch(url)
          # print(response)

          # transaction.delete()
          # for passenger in passengers:
          #      passenger.delete()
          booking.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)

# ======================================Booking History ================================

class BookingInsertandGettingall(GenericAPIView,CreateModelMixin,ListModelMixin):
     queryset = BookingHistory.objects.all()
     serializer_class=BookingHistorySerializer
     
     def post(self,request):
          logger.info("=  {} ".format(request.data))
          return self.create(request)
     def get(self,request):
          logger.info("==  {} ".format(request.data))
          return self.list(request)



class BookingUpadateAndDeleteAndRetraiveByID(GenericAPIView,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin,ListModelMixin):
     queryset=BookingHistory.objects.all()
     serializer_class=BookingHistorySerializer
     def put(self,request,**kwargs):
          logger.info("===  {} ".format(request.data))
          return self.update(request,**kwargs)
     def delete(self,request,**kwargs):
          logger.info("====  {} ".format(request.data))
          return self.destroy(request,**kwargs)
     def get(self,request,**kwargs):
          logger.info("=====  {} ".format(request.data))
          return self.list(request,**kwargs)
