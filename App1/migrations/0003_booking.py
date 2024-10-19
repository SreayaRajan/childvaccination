# Generated by Django 5.0.7 on 2024-10-19 11:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0002_profile_address_profile_child_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccinations', models.CharField(max_length=100)),
                ('appointment_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('token_number', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('Upcoming', 'Upcoming'), ('Cancelled', 'Cancelled'), ('Rejected', 'Rejected'), ('Refunded', 'Refunded'), ('Completed', 'Completed')], default='Upcoming', max_length=10)),
                ('payment_method', models.CharField(default='razorpay', editable=False, max_length=10)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
