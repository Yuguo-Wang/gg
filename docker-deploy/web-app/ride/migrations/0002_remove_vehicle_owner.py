# Generated by Django 4.1.5 on 2023-02-02 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='owner',
        ),
    ]
