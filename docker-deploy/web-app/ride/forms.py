from django import forms
from .models import Vehicle, Ride, ShareRide

class VehicleForm(forms.ModelForm):

    class Meta:
        model = Vehicle
        fields = ('plate_num', 'type', 'capacity', 'special_vehicle_info')
        widgets = {
            'plate_num': forms.TextInput(attrs={'required': True}),
            'capacity': forms.NumberInput(attrs={'required': True}),
        }

        
class RideForm(forms.ModelForm):

    class Meta:
        model = Ride
        fields = ('destination', 'arrival_time', 'number_of_passengers', 'shared', 'vehicle_type', 'special_request', )
        widgets = {
            'destination': forms.TextInput(attrs={'required': True}),
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'required': True},),
            'number_of_passengers': forms.NumberInput(attrs={'required': True}),
        }


class ShareRideForm(forms.ModelForm):

    class Meta:
        model = ShareRide
        fields = ('destination', 'earliest_time', 'latest_time', 'number_of_passengers')
        widgets = {
            'destination': forms.TextInput(attrs={'required': True}),
            'earliest_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'required': True}),
            'latest_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'required': True}),
            'number_of_passengers': forms.NumberInput(attrs={'required': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        earliest_time = cleaned_data.get('earliest_time')
        latest_time = cleaned_data.get('latest_time')
        if earliest_time and latest_time:
            if earliest_time >= latest_time:
                raise forms.ValidationError("Invalid arrival window!")
