from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import RideForm, ShareRideForm
from .models import Ride, ShareRide
from account.models import MyUser


def make_request(request):
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save()
            ride.owner = request.user
            ride.number_of_passengers_sum = ride.number_of_passengers
            request.user.owner_rides.add(ride)
            ride.save()
            request.user.save()
            return render(request, 'home.html')
        else:
            return render(request, 'edit_request.html', {'form':form})
    else:
        form = RideForm()
        args = {'form':form}
        return render(request, 'ride_request.html', args)
    
def edit_request(request, ride_id):
    ride = Ride.objects.get(pk=ride_id)
    p_num = ride.number_of_passengers
    if request.method == 'POST':
        form = RideForm(request.POST, instance=ride)
        if form.is_valid():
            form.save()
            ride.number_of_passengers_sum += ride.number_of_passengers - p_num
            ride.save()
            return redirect(reverse('show-my-rides'))
        else:
            return render(request, 'edit_request.html', {'form':form})
    else:
        form = RideForm(instance=ride)
        args = {'form':form}
        return render(request, 'edit_request.html', args)

def open_rides_drive(request):
    rides1 = Ride.objects.filter(
        driver=None, 
        special_request=request.user.vehicle.special_vehicle_info, 
        vehicle_type=request.user.vehicle.type, 
        number_of_passengers_sum__range=(0, request.user.vehicle.capacity))
    rides2 = Ride.objects.exclude(sharers=request.user)
    rides3 = Ride.objects.exclude(owner=request.user)
    rides = rides1 & rides2
    rides = rides & rides3
    return render(request, 'open_rides.html', {'rides':rides, 'mode': 'drive', 'share_ride_id': 0, 'back_url': 'open-rides-drive'})

def send_email(recipient_list):
    subject = 'Your ride has been confirmed!'
    message = 'Congratulations! Your ride has been confirmed by a SuperRide Driver! Please login to your account for more details.\n'
    from_email = 'superride_customer_service@outlook.com'
    for recipient in recipient_list:
        send_mail(subject, message, from_email, [recipient])

def drive_ride(request, ride_id):
    ride = Ride.objects.get(pk=ride_id)
    if request.method == 'POST':
        ride.status = 'CONFIRMED'
        ride.driver = request.user
        ride.save()
        users1 = MyUser.objects.filter(owner_rides=ride)
        users2 = MyUser.objects.filter(sharer_rides=ride)
        users = users1.union(users2)
        email_list = [user.email for user in users]
        send_email(email_list)
    return redirect(reverse('open-rides-drive'))

def open_rides_share(request):
    if request.method == 'POST':
        form = ShareRideForm(request.POST)
        if form.is_valid():
            share_ride = form.save()
            share_ride.owner = request.user
            share_ride.save()
            dest = share_ride.destination
            e_time = share_ride.earliest_time
            l_time = share_ride.latest_time
            rides1 = Ride.objects.exclude(driver=request.user)
            rides2 = Ride.objects.exclude(owner=request.user)
            rides3 = Ride.objects.exclude(sharers=request.user)
            rides4 = Ride.objects.filter(
                shared=True,
                status='OPEN',
                destination=dest, 
                arrival_time__range=(e_time, l_time)
            )
            rides = rides1 & rides2
            rides = rides & rides3
            rides = rides & rides4
            args = {'rides':rides, 'mode': 'share', 'share_ride_id': share_ride.pk, 'back_url': 'open-rides-share'}
            return render(request, 'open_rides.html', args)
        else:
            return render(request, 'open_rides.html', {'form': form, 'mode': 'share'})
    else:
        form = ShareRideForm()
    return render(request, 'open_rides.html', {'form': form, 'mode': 'share'})

def share_ride(request, ride_id, share_ride_id):
    ride = Ride.objects.get(pk=ride_id)
    share_ride = ShareRide.objects.get(pk=share_ride_id)
    if request.method == 'POST':
        request.user.sharer_rides.add(ride)
        share_ride.ride = ride
        ride.number_of_passengers_sum += share_ride.number_of_passengers
        share_ride.save()
        ride.save()
        request.user.save()
    return redirect(reverse('show-my-rides', kwargs={'mode': 'all'}))

def complete_ride(request, ride_id):
    ride = Ride.objects.get(pk=ride_id)
    if request.method == 'POST':
        ride.status = 'COMPLETE'
        ride.save()
    return redirect(reverse('show-my-rides', kwargs={'mode': 'all'}))

def quit_ride(request, ride_id):
    ride = Ride.objects.get(pk=ride_id)
    share_ride = ShareRide.objects.filter(ride=ride, owner=request.user)[0]
    if request.method == 'POST':
        ride.number_of_passengers_sum -= share_ride.number_of_passengers
        request.user.sharer_rides.remove(ride)
        ride.save()
        request.user.save()
        share_ride.delete()
    return redirect(reverse('show-my-rides', kwargs={'mode': 'all'}))

def display_my_rides(request, mode):
    owner_rides = request.user.owner_rides.exclude(status='COMPLETE')
    driver_rides = request.user.driver_rides.exclude(status='COMPLETE')
    sharer_rides = request.user.sharer_rides.exclude(status='COMPLETE')
    if mode == 'owner':
        my_rides = owner_rides
    elif mode == 'sharer':
        my_rides = sharer_rides
    elif mode == 'driver':
        my_rides = driver_rides
    else:
        my_rides = owner_rides.union(driver_rides)
        my_rides = my_rides.union(sharer_rides)
    args = {'rides':my_rides, }
    return render(request, 'my_rides.html', args)

def view_ride(request, ride_id, mode, share_ride_id, back_url):
    ride = Ride.objects.get(pk=ride_id)
    is_owner = ride.owner == request.user
    is_driver = ride.driver == request.user
    is_sharer = request.user in ride.sharers.all()
    owner = MyUser.objects.filter(owner_rides=ride)
    sharer_rides = ShareRide.objects.filter(ride=ride)
    if is_owner:
        role = 'Owner'
    elif is_driver:
        role = 'Driver'
    elif is_sharer:
        role = 'Sharer'
    else:
        role = 'Guest'
    args = {'ride':ride, 'owner': owner, 'sharer_rides': sharer_rides, 'role': role, 'mode': mode, 'share_ride_id': share_ride_id, 'back_url': back_url}
    return render(request, 'ride_detail.html', args)