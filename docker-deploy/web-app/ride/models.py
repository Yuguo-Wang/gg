from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

CAR_TYPES = [
    ('NONE', 'Unknown'),
    ('SEDAN', 'Sedan'),
    ('COUPE', 'Coupé'),
    ('CONV','Convertible'),
    ('SUV', 'SUV'),
    ('VAN', 'Van'),
    ('WAGON', 'Wagon'),
    ('SPORT', 'Sports car'),
    ('OTHER', 'Other'),
]

def validate_not_earlier_than_now(value):
    if value < timezone.now():
        raise ValidationError("Date must not be earlier than current time")

class Ride(models.Model):
    owner = models.ForeignKey('account.MyUser', on_delete=models.CASCADE, blank=True, null=True, related_name='owner_rides')
    driver = models.ForeignKey('account.MyUser', on_delete=models.CASCADE, blank=True, null=True, related_name='driver_rides')
    destination = models.CharField(max_length=100, blank=True, null=True)
    arrival_time = models.DateTimeField(validators=[validate_not_earlier_than_now], blank=True, null=True)
    number_of_passengers = models.IntegerField(blank=True, null=True)
    number_of_passengers_sum = models.IntegerField(blank=True, null=True)
    shared = models.BooleanField(default=False)
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETE', 'Complete'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    vehicle_type = models.CharField(max_length=5, choices=CAR_TYPES, default='NONE')
    special_request = models.CharField(max_length=200, blank=True, null=True)

class ShareRide(models.Model):
    destination = models.CharField(max_length=100, blank=True, null=True)
    earliest_time = models.DateTimeField(validators=[validate_not_earlier_than_now], blank=True, null=True)
    latest_time = models.DateTimeField(validators=[validate_not_earlier_than_now], blank=True, null=True)
    number_of_passengers = models.IntegerField(blank=True, null=True)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey('account.MyUser', on_delete=models.CASCADE, blank=True, null=True, related_name='share_rides_detail')

class Vehicle(models.Model):
    plate_num = models.CharField(max_length=10, verbose_name='Plate number',blank=True, null=True)
    type = models.CharField(max_length=5, choices=CAR_TYPES, default='NONE')
    capacity = models.IntegerField(blank=True, null=True)
    special_vehicle_info = models.CharField(max_length=200, blank=True, null=True)
