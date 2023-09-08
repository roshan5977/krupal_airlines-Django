# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Flight(models.Model):
    flight_number = models.IntegerField(blank=False)
    seating_capacity = models.IntegerField(blank=False)
    status = models.CharField(max_length=45, default='Active',blank=False)

    class Meta:
        db_table = 'flight'


class Airport(models.Model):
    airport_name = models.CharField(max_length=255,blank=False)
    city = models.CharField(max_length=45,blank=False)
    status = models.CharField(max_length=45, default='Active',blank=False)

    class Meta:
        db_table = 'airport'

class Schedule(models.Model):
    source_airport = models.ForeignKey(
        Airport, models.DO_NOTHING, db_column='source_airport', related_name='source_schedules',blank=False)
    destination_airport = models.ForeignKey(
        Airport, models.DO_NOTHING, db_column='destination_airport', related_name='destination_schedules',blank=False)
    arrival_time = models.DateTimeField(blank=False)
    departure_time = models.DateTimeField(blank=False)
    available_seats = models.IntegerField(blank=False)
    base_price = models.FloatField(blank=False)
    flight = models.ForeignKey(Flight, on_delete=models.DO_NOTHING,blank=False)
    status = models.CharField(max_length=45, default='Active',blank=False)
    
    class Meta:
        db_table = 'schedule'
