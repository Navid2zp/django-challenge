# Generated by Django 3.1.5 on 2021-01-17 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stadiums', '0006_auto_20210117_1541'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stadiumseat',
            unique_together={('seat_row', 'seat_column', 'stadium')},
        ),
        migrations.RemoveField(
            model_name='stadiumseat',
            name='seat_code',
        ),
    ]
