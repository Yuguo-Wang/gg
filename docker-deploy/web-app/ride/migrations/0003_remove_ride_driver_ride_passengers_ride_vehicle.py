# Generated by Django 4.1.5 on 2023-02-02 02:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ride', '0002_remove_vehicle_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ride',
            name='driver',
        ),
        migrations.AddField(
            model_name='ride',
            name='passengers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Passengers'),
        ),
        migrations.AddField(
            model_name='ride',
            name='vehicle',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, to='ride.vehicle', verbose_name='Vehicle'),
        ),
    ]
