 # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login.models import Login
from datetime import datetime

# Create your models here.
class TripManager(models.Manager):
    def create_trip(self, data, id):
        current_date = datetime.now().strftime('%Y-%m-%d')
        errors = []
        if len(data['destination']) < 2:
            errors.append(['destination', "Destination name must be at least two characters in length."])
        if data['description'] == "":
            errors.append(['description', "Please enter a description."])
        if data['travelDateFrom'] < current_date:
            errors.append(['description', "Please enter a departure date greater than or equal to today's date."])
        if data['travelDateTo'] <= data['travelDateFrom']:
            errors.append(['description', "Please enter a return date greater than your departure date."])
        if errors:
            return [False, errors]
        else:
            user_id = Login.objects.get(id=id)
            NewTrip = Trip(destination=data['destination'], description=data['description'], user_id=user_id, travelDateFrom=data['travelDateFrom'], travelDateTo=data['travelDateTo'])
            NewTrip.save()
            myTrip = Travel(trip_id=Trip.objects.last(), user_id=user_id)
            myTrip.save()
            return [True, myTrip]

class Trip(models.Model):
    destination = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    travelDateFrom = models.DateField()
    travelDateTo = models.DateField()
    user_id = models.ForeignKey('login.Login', related_name='planner', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()

    def __str__(self):
        return 'ID: %s | Destination: %s | Description: %s | Departure: %s | Return: %s | Created: %s | Updated: %s' % (self.id, self.destination, self.description, self.travelDateFrom, self.travelDateTo, self.created_at, self.updated_at)

class TravelManager(models.Manager):
    def join_trip(self, user_id, trip_id):
        user_id = Login.objects.get(id=user_id)
        trip_id = Trip.objects.get(id=trip_id)
        Travel.objects.create(user_id=user_id, trip_id=trip_id)

class Travel(models.Model):
    user_id = models.ForeignKey('login.Login', related_name='PersonTraveling', on_delete=models.CASCADE)
    trip_id = models.ForeignKey('travelbuddy.Trip', related_name='TripSelected', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TravelManager()

    def __str__(self):
        return 'ID: %s | User ID: %s | Trip ID: %s | Created: %s | Updated: %s' % (self.id, self.user_id, self.trip_id, self.created_at, self.updated_at)
