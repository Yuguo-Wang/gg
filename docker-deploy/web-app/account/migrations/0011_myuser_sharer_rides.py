# Generated by Django 4.1.5 on 2023-02-03 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0008_ride_driver_alter_ride_arrival_time_alter_ride_owner'),
        ('account', '0010_alter_myuser_email_alter_myuser_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='sharer_rides',
            field=models.ManyToManyField(blank=True, null=True, to='ride.ride'),
        ),
    ]
