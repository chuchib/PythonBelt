from __future__ import unicode_literals

from django.db import models
import bcrypt, re

EMAIL_REGEX =re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$')

# Create your models here.
class LoginManager(models.Manager):
    #Validations
    def validate_create(self,data):
        print data, "Data from validations"

        replicated = Login.objects.filter(email=data['email'])
        errors =[]

        if len(data['first_name'])<2:
            print "First name is too short"
            errors.append("First name is too short")

        if len(data['last_name'])<2:
            print "last name too short"
            errors.append("Last name is too short")
        if len(data['email'])<1:
            print "email is blank"
            errors.append("Email cannot be empty")
        if not EMAIL_REGEX.match(data['email']):
            errors.append("Email invalid")
        if len(replicated) > 0:
            print "Email has already been registered"
            errors.append("Email has already been registered")
        if len(data['password'])<1:
            errors.append("Password is required")
        elif len(data['password'])<6:
            errors.append("Password must be at least 6 characters")
        if data['password'] != data ['password_confirmation']:
            errors.append("Passwords must match")
        if errors:
            return(False, errors)
        else:
            #try:
                #self.get(email= data ['email'])
                #errors.append('Email is already registered')
                #return(False, errors)

            #except:
            new_user = Login.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password= bcrypt.hashpw(data['password'].encode(),bcrypt.gensalt())
            )
            return(True, new_user)

    def validate_login(self, data):

        User_Exists = Login.objects.filter(email=data['email'])
        errors=[]

        if len(data['email'])<1:
            errors.append('Email is required')
        if not EMAIL_REGEX.match(data['email']):
            errors.append('Must be an email address')
        if len(User_Exists)== 0:
            print "Email is not registered"
            errors.append("Email is not registered")
        if len(data['password'])<1:
            errors.append('password must be entered')
        if errors:
            return (False, errors)
        else:
            login_user = Login.objects.get(email=data['email'])
            pw = data['password']

            # hashed_pw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
            if bcrypt.hashpw(pw.encode(), login_user.password.encode()) == login_user.password.encode():
            # if bcrypt.checkpw(pw.encode(), login_user.password.encode()):
                print "the passwords match"
                return (True, login_user)
            else:
                print "the passwords DONT match"
                errors.append("Invalid Password")
                return (False, errors)
        #if not errors:
            #try:
                #user = Login.objects.get(email=data['email'])
                #if bcrypt.hashpw(data['pw'].encode(), user.password.encode()) == user.password.encode():
                    #return (True, user)
            #except:
                #errors.append('Invalid login')
                #return (False, errors)


class Login(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = LoginManager()

    def __str__(self):
        return 'ID: %s | Name: %s %s | Email: %s | Created: %s | Updated: %s' % (self.id, self.first_name, self.last_name, self.email, self.created_at, self.updated_at)
