# Generated by Django 5.0.7 on 2024-07-12 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_booked_date_bookingdata_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookingdata',
            old_name='date',
            new_name='booked_date',
        ),
    ]
