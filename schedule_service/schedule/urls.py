from django.urls import path
from schedule.views import *

urlpatterns = [
  
    path('AirportInsertandGettingall/',AirportInsertandGettingall.as_view(),name="AirportInsertandGettingall"),
    path('updateAndDeleteAndRetraiveByID/<int:pk>/',updateAndDeleteAndRetraiveByID.as_view(),name="updateAndDeleteAndRetraiveByID"),
    path('FlightInsertandGettingall/',FlightInsertandGettingall.as_view(),name="FlightInsertandGettingall"),
    path('FlightupdateAndDeleteAndRetraiveByID/<int:pk>/',FlightupdateAndDeleteAndRetraiveByID.as_view(),name="FlightupdateAndDeleteAndRetraiveByID"),
    path('inserting/', inserting,name='inserting'),
    path('gettingData/', gettingData,name='gettingData'),
    path('getById/<int:id>/', getById,name='getById'),
    path('updateSchedule/<int:id>/',updateSchedule ,name='updateSchedule'),
    path('deleteSchedule/<int:id>/', deleteSchedule,name='deleteSchedule'),
    path('patchAirport/<int:id>/',patchAirport,name='patchAirport'),
    path('patchFlight/<int:id>/',patchFlight,name='patchFlight'),
    path('patchSchedule/<int:id>/',patchSchedule,name='patchSchedule'),
    path('patchAvailableTickets/<int:id>/<int:available_seats>/',patchAvailableTickets,name='patchAvailableTickets'),
    path('patchScheduleByTime/<int:id>/',patchScheduleByTime,name='patchScheduleByTime'),
]
