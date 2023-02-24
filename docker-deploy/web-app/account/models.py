from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    vehicle = models.OneToOneField('ride.Vehicle', on_delete=models.RESTRICT,verbose_name="My Vehicle", default=None, null=True, blank=True)
    is_driver = models.BooleanField(default=False, verbose_name="Is a Driver")
    phone_number = models.CharField(max_length=10, default=None, null=True, blank=True)
    sharer_rides = models.ManyToManyField('ride.Ride', blank=True, related_name='sharers')

    def __str__(self):
        return self.username


 
