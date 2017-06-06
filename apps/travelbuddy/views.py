# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from . models import Trip, Travel
from ..login.models import Login

# Create your views here.
def index(request):
    return render(request, "travelbuddy/index.html")

def travels(request):
    if 'user' not in request.session:
        return redirect('travelbuddy:index')
    context = {
        "user_trips": Travel.objects.all().order_by('trip_id__travelDateFrom'),
    }
    return render(request, "travelbuddy/travels.html", context)

def trip_add(request):
    if 'user' not in request.session:
        return redirect('travelbuddy:index')
    return render(request, "travelbuddy/trip_add.html")

def create_trip(request):
    if request.method == "POST":
        response = Trip.objects.create_trip(request.POST, request.session['user']['id'])
    if not response[0]:
        for error in response[1]:
            messages.error(request, error[1])
        return redirect('travelbuddy:trip_add')
    else:
        return redirect('travelbuddy:travels')

def join_trip(request, trip_id):
    Travel.objects.join_trip(request.session['user']['id'], trip_id)
    return redirect('travelbuddy:travels')

def destination(request, id):
    if 'user' not in request.session:
        return redirect('travelbuddy:index')
    try:
        destination_check = Travel.objects.get(id=id)
    except:
        return redirect('travelbuddy:travels')
    if request.method == 'GET':
        context = {
            "destination": Trip.objects.order_by(id).get(id=id),
            "userTrips": Travel.objects.all(),
        }
        return render(request, "travelbuddy/destination.html", context)
