from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import (
    CustomUserCreationForm, BasicUserChangeForm, DriverProfForm, NonDriverForm
)
from ride.forms import VehicleForm
from ride.models import Ride


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def myprof(request):
    if request.user.driver_rides.exclude(status='COMPLETE'):
        can_edit = False
    else:
        can_edit = True
    return render(request, "my_prof.html", {'can_edit':can_edit})

def driver_register(request):
    if request.method == 'POST':
        user_form = DriverProfForm(request.POST, instance=request.user)
        vehicle_form = VehicleForm(request.POST)
        if user_form.is_valid() and vehicle_form.is_valid():
            vehicle = vehicle_form.save()
            request.user.vehicle = vehicle
            request.user.is_driver = True
            user_form.save()
            request.user.save()
            return redirect('/account/profile')
        else:
            args = {'u_form':user_form, 'v_form':vehicle_form}
            return render(request, 'driver_reg.html', args)
    else:
        user_form = DriverProfForm(instance=request.user)
        vehicle_form = VehicleForm()
        args = {'u_form':user_form, 'v_form':vehicle_form}
        return render(request, 'driver_reg.html', args)

def quit_driver(request):
    if request.method == 'POST':
        request.user.is_driver = False
        request.user.save()
    return redirect('/account/profile')

def edit_profile(request):
    if request.method == 'POST':
        basic_form = BasicUserChangeForm(request.POST, instance=request.user)
        if (request.user.is_driver):
            driver_form = DriverProfForm(request.POST, instance=request.user)
        else:
            driver_form = NonDriverForm(request.POST, instance=request.user)
        if basic_form.is_valid() and driver_form.is_valid():
            basic_form.save()
            driver_form.save()
            return redirect('/account/profile')
        else:
            args = {'b_form':basic_form, 'd_form':driver_form}
            return render(request, 'edit_profile.html', args)

    else:
        basic_form = BasicUserChangeForm(instance=request.user)
        if (request.user.is_driver):
            driver_form = DriverProfForm(instance=request.user)
        else:
            driver_form = NonDriverForm(instance=request.user)
        args = {'b_form':basic_form, 'd_form':driver_form}
        return render(request, 'edit_profile.html', args)

def edit_vehicle_info(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=request.user.vehicle)
        if form.is_valid():
            form.save()
            return redirect('/account/profile')
        else:
            return render(request, 'edit_vehicle.html', {'form':form})
    else:
        form = VehicleForm(instance=request.user.vehicle)
        args = {'form':form}
        return render(request, 'edit_vehicle.html', args)

def passwd_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/account/profile')
        else:
            return render(request, 'passwd_change.html', {'form':form})
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request, 'passwd_change.html', args)