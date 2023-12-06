import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.expressions import F
User._meta.get_field('email')._unique = True
User._meta.get_field('email')._blank = False
User._meta.get_field('email')._null = False

class Driver(models.Model):
	driver_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200,null=False)
	phone_number = models.CharField(max_length=200,null=False)
	licenese_number = models.CharField(max_length=200,null=False)

class Request(models.Model):
    request_id = models.AutoField(primary_key=True)
    user_email=models.ForeignKey(User,on_delete= models.CASCADE)
    departure_time = models.DateTimeField(null=False)
    startpoint=models.CharField(max_length=300,null=False)
    endpoint=models.CharField(max_length=300,null=False)
    number_seats=models.IntegerField(null=False)

    def __str__(self):
        return str(self.request_id)    

class Bus(models.Model):
    bus_id = models.AutoField(primary_key=True)
    driver_id = models.ForeignKey(Driver, null=True, on_delete= models.CASCADE)
    availability = models.BooleanField(default=True)
    capacity = models.IntegerField(null=False)

    def __str__(self):
        return str(self.bus_id)    


class Schedule(models.Model):
    CATEGORY = (
			('Sunday', 'Sunday'),
			('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thrusday', 'Thrusday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
			) 
    schedule_id = models.AutoField(primary_key=True)
    bus_id = models.ForeignKey(Bus, null=True, on_delete= models.CASCADE)
    time = models.TimeField(null=False)
    start = models.CharField(max_length=300,null=False)
    destination=models.CharField(max_length=300,null=False)
    available_seats = models.IntegerField(null=False)
    day= models.CharField(max_length=200,null=False,choices=CATEGORY)
    running_status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.schedule_id)

class Wallet(models.Model):
    wallet_id = models.OneToOneField(User, primary_key=True,on_delete= models.CASCADE)
    balance = models.IntegerField(null=False)

    def _str_(self):
        return str(self.wallet_id)

class Booking(models.Model):
    booking_id=models.AutoField(primary_key=True)
    user_email=models.ForeignKey(User,on_delete= models.CASCADE)
    date_time=models.DateTimeField(null=True)
    seat_no=models.IntegerField(null=False)
    schedule_id=models.ForeignKey(Schedule,null=False,on_delete= models.CASCADE)
    refund_status=models.BooleanField(default=False)

    def _str_(self):
        return 'BOOK#00'+str(self.booking_id)  


class AdminUser(models.Model):
    admin_id = models.OneToOneField(User,null=True,on_delete= models.CASCADE)
    email = models.CharField(max_length=50,null=False)

    def _str_(self):
        return str(self.Admin_id)

