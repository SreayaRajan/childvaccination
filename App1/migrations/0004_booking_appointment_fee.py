# Generated by Django 5.0.7 on 2024-10-19 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0003_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='appointment_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=10),
        ),
    ]
