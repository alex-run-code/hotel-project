# Generated by Django 3.2 on 2021-04-29 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0006_auto_20210429_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinginfo',
            name='hotel_room_type',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booking_info', to='listings.hotelroomtype'),
        ),
        migrations.AlterField(
            model_name='bookinginfo',
            name='listing',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booking_info', to='listings.listing'),
        ),
    ]
