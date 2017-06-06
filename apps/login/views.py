from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from . models import Login
import bcrypt
import re
EMAILREG = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


# Create your views here.
#def index(request):
    #print "Inside index def"

    # For displaying all login records (just for testing).
    #context = {
        #'logins': Login.objects.all()
    #}
    #return render(request, "login/index.html", context)

def log_register(request):
    if request.method == "POST":
        if request.POST["carryon"] == "register":
            response = Login.objects.validate_create(request.POST)
        elif request.POST["carryon"] == "login":
            response = Login.objects.validate_login(request.POST)
        if not response[0]:
            for error in response[1]:
                messages.error(request, error)
            return redirect('travelbuddy:index')
        else:
            request.session['user'] = {
            "id": response[1].id,
            "first_name": response[1].first_name,
            "last_name": response[1].last_name,
            }
            current_user = response[1].id
            return redirect('travelbuddy:travels')
    return redirect('travelbuddy:index')
   
def login(request):
    print "Login route success"

    if request.method =='POST':
        print request.POST

        valid, data = Login.objects.validate_login(request.POST)

        if valid == True:
            print"Login successful"
            print "*******"
        else:
            for err in data:
                messages.error(request, err)
            return redirect('/')

    context = {
            'logins': Login.objects.all()
    }
    #saving info to success page in session
    user_info = Login.objects.validate_login(request.POST)
    request.session['first_name'] = user_info[1].first_name

    return render (request, "login/success.html", context)

def logout(request):
    print "logout route"
    print "***********"
    request.session.clear()
    return redirect('travelbuddy:index')
