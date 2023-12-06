from datetime import datetime
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.
from .models import *
from .forms import CreateUserForm
from datetime import date
import calendar
import datetime


def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
	context = {'form':form}
	return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            login_obj = AdminUser.objects.filter(admin_id = user).first()
            if login_obj:
                return redirect('/admin_home')
            else:    
                return redirect('/home')
        else:
            messages.info(request, 'username OR password incorrect')
    return render(request, 'accounts/login.html')

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def driver(request):
    user=request.user
    login_obj = AdminUser.objects.filter(admin_id = user).first()
    if login_obj:
        allD=Driver.objects.all()
        context={'allD': allD} 
        return render(request,'accounts/driver.html',context)
    return redirect('/')

@login_required(login_url='login')
def add_driver(request):
    user=request.user
    login_obj = AdminUser.objects.filter(admin_id = user).first()
    if login_obj:
        if request.method == 'POST':
                if request.POST.get('name') and request.POST.get('phone_number') and request.POST.get('licenese_number'):
                    post=Driver()
                    post.name= request.POST.get('name')
                    post.phone_number= request.POST.get('phone_number')
                    post.licenese_number= request.POST.get('licenese_number')
                    post.save()
                
                    return render(request, 'accounts/add_driver.html')  
        else:
            return render(request,'accounts/add_driver.html')
    return redirect('/')

@login_required(login_url='login')
def home(request):
    return render(request, 'accounts/user_home.html')
   
@login_required(login_url='login')
def admin_home(request):
    user=request.user
    login_obj = AdminUser.objects.filter(admin_id = user).first()
    if login_obj:
        return render(request,'accounts/admin_home.html')
    return redirect('/')

@login_required(login_url='login')
def delete_driver(request,id):
    user=request.user
    login_obj = AdminUser.objects.filter(admin_id = user).first()
    if login_obj:
        obj=Driver.objects.get(driver_id=id)
        obj.delete()
        return redirect('driver')
    return redirect('/')

@login_required(login_url = 'login')
def add_request(request):
    if request.method == 'POST':
            if request.POST.get('departure_time') and request.POST.get('startpoint') and request.POST.get('endpoint') and request.POST.get('number_seats'):
                post = Request()
                name = request.user.email
                user_obj = User.objects.filter(email = name).first()
                post.user_email = user_obj
                post.departure_time = request.POST.get('departure_time')
                post.startpoint = request.POST.get('startpoint')
                post.endpoint = request.POST.get('endpoint')
                post.number_seats = request.POST.get('number_seats')
                curr_datetime = datetime.datetime.now()

                # May need to change for different local format
                given_datetime = datetime.datetime.strptime(post.departure_time, '%Y-%m-%dT%H:%M') 
                
                if(int(post.number_seats)>2^23-1):
                    messages.error(request, 'Invalid seat number')
                elif (int(post.number_seats) > 0 and given_datetime > curr_datetime):
                    post.save()
                    messages.success(request, 'Request sent successfully')
                elif(int(post.number_seats) < 1 and given_datetime <= curr_datetime):
                    messages.error(request, 'Request falied! Invalid Number of Seats and Invalid Time')
                elif(int(post.number_seats) < 1):
                    messages.error(request, 'Request falied! Invalid number of seats')
                elif(given_datetime <= curr_datetime):
                    messages.error(request, 'Request falied! Invalid Time')
                else:
                    assert(0)

                return render(request, 'accounts/add_request.html')  
    else:
        return render(request,'accounts/add_request.html')

@login_required(login_url='login')
def request(request):
    user=request.user
    login_obj = AdminUser.objects.filter(admin_id = user).first()
    if login_obj:
        allD=Request.objects.all()
        context={'allD': allD} 
        return render(request,'accounts/request.html',context)
    return redirect('/')

@login_required(login_url='login')
def add_bus(request):
    user=request.user
    login_obj = AdminUser.objects.filter(admin_id = user).first()
    if login_obj:
        if request.method == 'POST':
            if request.POST.get('availability') and request.POST.get('capacity') and request.POST.get('driver_id'):
                post=Bus()
                post.availability= request.POST.get('availability')
                post.capacity= request.POST.get('capacity')
                name=request.POST.get('driver_id')
                driver_obj = Driver.objects.filter(driver_id = name).first()
                post.driver_id = driver_obj
                post.save()
                return render(request,'accounts/add_bus.html')
        else:
            return render(request,'accounts/add_bus.html')
    return redirect('/')

@login_required(login_url='login')
def bus(request):
    user=request.user
    login_obj = AdminUser.objects.filter(admin_id = user).first()
    if login_obj:
        allD=Bus.objects.all()
        context={'allD': allD} 
        return render(request,'accounts/bus.html',context)
    return redirect('/')

@login_required(login_url='login')
def delete_bus(request,id):
    user=request.user
    login_obj = AdminUser.objects.filter(admin_id = user).first()
    if login_obj:
        obj=Bus.objects.get(bus_id=id)
        obj.delete()
        return redirect('bus')
    return redirect('/')

@login_required(login_url='login')
def add_schedule(request):
    user=request.user
    login_obj = AdminUser.objects.filter(admin_id = user).first()
    if login_obj:
        if request.method == 'POST':
                if request.POST.get('time') and request.POST.get('start') and request.POST.get('destination')  and request.POST.get('available_seats')  and request.POST.get('day') and request.POST.get('running_status') and request.POST.get('bus_id'):
                    post=Schedule()
                    bus_id=request.POST.get('bus_id')
                
                    bus_obj = Bus.objects.filter(bus_id = bus_id).first()
                    post.bus_id= bus_obj
                    post.time= request.POST.get('time')
                    post.start= request.POST.get('start')
                    post.destination= request.POST.get('destination')
                    post.available_seats= request.POST.get('available_seats')
                    post.day= request.POST.get('day')
                    post.running_status= request.POST.get('running_status')
                    post.save()
                    return render(request, 'accounts/add_schedule.html')  
        else:
             return render(request, 'accounts/add_schedule.html')  
    return redirect('/')

@login_required(login_url='login')
def view_schedule(request):
    user=request.user
    login_obj = AdminUser.objects.filter(admin_id = user).first()
    if login_obj:
        allD=Schedule.objects.all()
        context={'allD': allD} 
        return render(request,'accounts/View_schedule.html',context)
    return redirect('/')

@login_required(login_url='login')
def delete_schedule(request,id):
    user=request.user
    login_obj = AdminUser.objects.filter(admin_id = user).first()
    if login_obj:
        obj=Schedule.objects.get(schedule_id=id)
        date=timezone.now().date()
        curr_date = date.today()
        curr_day = calendar.day_name[curr_date.weekday()]
        if curr_day == obj.day:
            booking_id = Booking.objects.filter(schedule_id = id).all()
            size1 = booking_id.count()
            i=0
            while i<size1:      
                date = booking_id[i].date_time.date()
                if date==curr_date:
                        book=booking_id[i].user_email
                        user = User.objects.filter(username=book).first() 
                        send_mail(
                            'Deleted Schedule',
                            'The schedule has been deleted.Therefore your booking has been cancelled.Thank you',
                            settings.EMAIL_HOST_USER,
                            [user.email],
                        
                            fail_silently=False,
                            ) 
                        seat_no = booking_id[i].seat_no
                        wallet_obj = Wallet.objects.filter(wallet_id = user).first()
                        wallet_obj.balance = wallet_obj.balance + (25*int(seat_no)) 
                        wallet_obj.save()
                        
                        booking_id[i].delete()
                        i=i+1
            obj.running_status=False
            obj.save()            
            messages.info(request, 'The schedule has been deleted')
            return redirect('/view_schedule')
        obj.running_status=False
        obj.save()
        return redirect('add_schedule')
    return redirect('/')


@login_required(login_url='login')
def update_schedule(request,id):
    if request.method == 'POST':
            if request.POST.get('time') and request.POST.get('start') and request.POST.get('destination') and request.POST.get('bus_id') and request.POST.get('running_status'):
                    post = Schedule.objects.filter(schedule_id = id).first()
                    bus_id=request.POST.get('bus_id')
                    bus_obj = Bus.objects.filter(bus_id = bus_id).first()
                    post.bus_id= bus_obj
                    post.time= request.POST.get('time')
                    post.start= request.POST.get('start')
                    post.destination= request.POST.get('destination')
                    post.running_status= request.POST.get('running_status')
                    date=timezone.now().date()
                    curr_date = date.today()
                    booking_id = Booking.objects.filter(schedule_id = id).all()
                    post.save()
                    size1 = booking_id.count()
                    i=0
                    while i<size1:
                        date = booking_id[i].date_time.date()
                        if date==curr_date:
                            book=booking_id[i].user_email
                            user = User.objects.filter(username=book).first()

                            print(user.email)
                            context={'post':post,'user':user}
                            template=render_to_string('accounts/email_template4.html',context)
                            send_mail(
                                'Updated Schedule',
                                template,
                                settings.EMAIL_HOST_USER,
                                [user.email],
                        
                                fail_silently=False,
                            )
                            i=i+1
                   
                    
                    messages.info(request,'Schedule is updated')
                    return render(request, 'accounts/view_schedule.html')  
    else:
        
        seats_obj = Schedule.objects.filter(schedule_id = id).first()
        bus_id=seats_obj.bus_id
        time=seats_obj.time
        start=seats_obj.start
        destination=seats_obj.destination
        running_status = seats_obj.running_status
        context={'bus_id':bus_id,'time':time,'start':start,'destination':destination,'running_status':running_status}
        return render(request,'accounts/update_schedule.html',context)


@login_required(login_url='login')
def add_wallet(request):
    user=request.user
    login_obj = AdminUser.objects.filter(admin_id = user).first()
    if login_obj:
        if request.method == 'POST':
                if request.POST.get('wallet_id') and request.POST.get('balance'):
                    post=Wallet()
                    wallet_id=request.POST.get('wallet_id')
                    bus_obj = User.objects.filter(email = wallet_id).first()
                   
                    post.wallet_id= bus_obj
                    wallet_obj = Wallet.objects.filter(wallet_id = bus_obj).first()
                    bal= request.POST.get('balance')
                    if(wallet_obj is None):
                              post.balance = int(bal)
                    else:
                      post.balance = wallet_obj.balance+int(bal)
                    post.save()
                    wallet_obj = Wallet.objects.filter(wallet_id = bus_obj).first()
                    context={'bus_obj':bus_obj,'bal':bal,'wallet_obj':wallet_obj}
                    template=render_to_string('accounts/email_template3.html',context)
                    send_mail(
                            'Balance successfully added',
                            template,
                            settings.EMAIL_HOST_USER,
                            [bus_obj.email],
                        
                            fail_silently=False,
                            ) 
                    
                    return render(request, 'accounts/add_wallet.html')  
        else:
            return render(request,'accounts/add_wallet.html')
    return redirect('/')

@login_required(login_url='login')
def book_bus(request):
    date=timezone.now().date()
    curr_date = date.today()
    curr_day = calendar.day_name[curr_date.weekday()]
    allD=Schedule.objects.filter(day=curr_day)
    context={'allD': allD,'date':date,'curr_day':curr_day}
    return render(request,'accounts/Book_bus.html',context)

@login_required(login_url='login')
def booking(request,id):
    if request.method == 'POST':
            if request.POST.get('seat_no'):
                seats = request.POST.get('seat_no')
                amount = 25*(int(seats))
                user = request.user
                email = user.email
                i=1
                wallet_obj = Wallet.objects.filter(wallet_id = user).first()
                if int(wallet_obj.balance) < int(amount):
                    messages.error(request, 'Your Balance is low')
                    i=0
                seats_obj = Schedule.objects.filter(schedule_id = id).first()
                if int(seats)<0:
                    messages.error(request, 'Please enter correct seat number')
                    i=0
                if int(seats_obj.available_seats) < int(seats):
                    messages.error(request, 'Seats are not available')
                    i=0
                if i==0:
                    return redirect('/book_bus')    
                wallet_obj.balance = wallet_obj.balance - int(amount)
                wallet_obj.save()
                seats_obj.available_seats = seats_obj.available_seats- int(seats)
                seats_obj.save()
                post=Booking()
                date = datetime.datetime.now()
                post.date_time = date
                bus_obj = User.objects.filter(email = email ).first()
                post.user_email= bus_obj
                post.seat_no= seats
                
                schedule_id=id
                bus_ob = Schedule.objects.filter(schedule_id = schedule_id ).first()
                post.schedule_id = bus_ob
                post.save()
                context={'user':user,'seats':seats,'wallet_obj':wallet_obj,'amount':amount}
                template=render_to_string('accounts/email_template.html',context)
                send_mail(
                            'Booking confirmed',
                            template,
                            settings.EMAIL_HOST_USER,
                            [user.email],
                        
                            fail_silently=False,
                            ) 
                messages.info(request,'Your seat is booked')
                return render(request, 'accounts/Past_bookings.html')
    else:
        user=request.user 
        seats_obj = Schedule.objects.filter(schedule_id = id).first()
        schedule_time = seats_obj.time
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        seats = seats_obj.available_seats
        wallet_obj = Wallet.objects.filter(wallet_id = user).first()
        if(current_time>(str(schedule_time))):
            messages.error(request,'bus is already gone')
            return redirect('/book_bus')
        if(wallet_obj is None):
            messages.error(request, 'You dont have wallet')
            return redirect('/book_bus')
        amount=wallet_obj.balance
        return render(request,'accounts/booking.html',{'seats' : seats,'amount':amount})

def schedule(request,data=None):
    if data==None:
        sch=Schedule.objects.filter(day='Monday')
        context={'sch': sch}
    elif data=='Monday':
        sch=Schedule.objects.filter(day='Monday')
        context={'sch': sch}
    elif data=='Tuesday':
        sch=Schedule.objects.filter(day='Tuesday')
        context={'sch': sch}
    elif data=='Wednesday':
        sch=Schedule.objects.filter(day='Wednesday')
        context={'sch': sch}
    elif data=='Thursday':
        sch=Schedule.objects.filter(day='Thursday')
        context={'sch': sch}
    elif data=='Friday':
        sch=Schedule.objects.filter(day='Friday')
        context={'sch': sch}
    elif data=='Saturday':
        sch=Schedule.objects.filter(day='Saturday')
        context={'sch': sch}
    elif data=='Sunday':
        sch=Schedule.objects.filter(day='Sunday')
        context={'sch': sch}
    return render(request, 'accounts/schedule.html',context)

@login_required(login_url='login')
def view_booking(request):
    user = request.user
    booking_obj = Booking.objects.filter(user_email = user).all()
    schedule_obj = Schedule.objects.all()
    return render(request,'accounts/Past_bookings.html',{'booking_obj' : booking_obj, 'schedule_obj' : schedule_obj})


def cancel_booking(request,id):
    if request.method == 'POST':
            if request.POST.get('seat_no'):
                user=request.user
                seats = request.POST.get('seat_no')
                booking_obj = Booking.objects.filter(booking_id = id).first()
                seat_no = booking_obj.seat_no
                if(int(seats)<0):
                    messages.error(request,'Invalid seat number')
                    return redirect('/view_booking')
                if(int(seats)>int(seat_no)):
                    messages.error(request,'You cannot cancel the seats more than the booked seat')
                    return redirect('/view_booking')
                wallet_obj = Wallet.objects.filter(wallet_id = user).first()
                balance = (25*int(seats))
                wallet_obj.balance = wallet_obj.balance + (25*int(seats)) 
                wallet_obj.save()
                sc_id = booking_obj.schedule_id
                schedule_obj = Schedule.objects.filter(schedule_id = str(sc_id)).first()
                schedule_obj.available_seats = schedule_obj.available_seats + int(seats)
                schedule_obj.save()
                booking_obj.refund_status = True
                booking_obj.seat_no = booking_obj.seat_no - int(seats)
                context={'user':user,'seats':seats,'wallet_obj':wallet_obj,'balance':balance}
                template=render_to_string('accounts/email_template2.html',context)
                send_mail(
                            'Booking cancelled',
                            template,
                            settings.EMAIL_HOST_USER,
                            [user.email],
                        
                            fail_silently=False,
                            ) 
                if booking_obj.seat_no is 0:
                    booking_obj.delete()
                    messages.info(request,'booking cancelled')
                    return redirect('/view_booking')
                booking_obj.save()
                messages.info(request,'booking cancelled')
                return render(request, 'accounts/Past_bookings.html')
    else:
        booking_obj = Booking.objects.filter (booking_id = id).first()
        booking_date = booking_obj.date_time.date()
        date=timezone.now().date()
        curr_date = date.today()
        sc_id = booking_obj.schedule_id
        schedule_obj = Schedule.objects.filter(schedule_id = str(sc_id)).first()
        schedule_time = schedule_obj.time 
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if curr_date>booking_date:
            messages.error(request,'You cannot cancel the booking')
            return redirect('/view_booking')
        if booking_obj.seat_no is 0:
            messages.error(request,'This booking is already cancelled')
            return redirect('/view_booking')
        if(current_time > (str(schedule_time))):
            messages.error(request,'You cannot cancel the booking')
            return redirect('/view_booking')
        seats = booking_obj.seat_no
        return render(request,'accounts/cancel_booking.html',{'seats' : seats})


	



