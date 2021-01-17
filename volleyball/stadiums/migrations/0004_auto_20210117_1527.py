# Generated by Django 3.1.5 on 2021-01-17 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stadiums', '0003_auto_20210117_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='stadiumseat',
            name='seat_column',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='stadiumseat',
            name='seat_row',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterUniqueTogether(
            name='stadiumseat',
            unique_together={('seat_row', 'seat_column'), ('stadium', 'seat_code')},
        ),
    ]
